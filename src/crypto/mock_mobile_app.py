import os
import json
import base64
from datetime import datetime, timezone
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def generar_llave_maestra():
    """Simula la generación o recuperación de la llave simétrica en el dispositivo."""
    # En la vida real, esta llave vendría de un intercambio seguro (ej. RSA)
    # o de un almacén de claves (Keystore/Keychain)
    return ChaCha20Poly1305.generate_key()

def simular_captura_app_movil():
    """Simula el formulario que llena el ganadero en la app móvil."""
    return {
        "id_reporte": f"REP-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "fecha_reporte": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        # Datos para NoSQL (Búsquedas, Modelos Epidemiológicos) - VAN EN TEXTO PLANO
        "datos_epidemiologicos": {
            "especie": "Bos taurus",
            "enfermedad_sospechosa": "Fiebre Aftosa (FMD)",
            "sintomas": ["Vesículas en boca y pezuñas", "Salivación excesiva", "Cojera"],
            "estado": "Jalisco",
            "numero_animales_afectados": 4
        },
        # Datos de Privacidad (Contacto, Ubicación exacta) - VAN CIFRADOS
        "datos_privacidad_plano": {
            "nombre_ganadero": "Juan Pérez",
            "telefono": "+52 33 1234 5678",
            "id_predio": "MX-JAL-1105",
            "coordenadas_gps": {"lat": 20.6596, "lon": -103.3496}
        }
    }

def cifrar_reporte(datos_completos, llave):
    """Aplica Field-Level Encryption usando ChaCha20-Poly1305."""
    
    chacha = ChaCha20Poly1305(llave)
    
    # 1. Generamos un nonce único (Number used ONCE) de 12 bytes
    nonce = os.urandom(12)
    
    # 2. Convertimos los datos sensibles a texto plano (JSON string) y luego a bytes
    datos_sensibles_json = json.dumps(datos_completos["datos_privacidad_plano"]).encode('utf-8')
    
    # 3. Ciframos los datos.
    # El método encrypt de ChaCha20Poly1305 retorna el texto cifrado + la etiqueta MAC (tag) concatenada.
    ciphertext_con_tag = chacha.encrypt(nonce, datos_sensibles_json, associated_data=None)
    
    # 4. Construimos el documento final para MongoDB (NoSQL)
    documento_seguro = {
        "id_reporte": datos_completos["id_reporte"],
        "fecha_reporte": datos_completos["fecha_reporte"],
        "datos_epidemiologicos": datos_completos["datos_epidemiologicos"],
        
        # Campo Cifrado (Bloque inescrutable para la base de datos)
        "datos_privacidad_ganadero": {
            "algoritmo": "ChaCha20-Poly1305",
            "nonce": base64.b64encode(nonce).decode('utf-8'),
            "ciphertext_and_tag": base64.b64encode(ciphertext_con_tag).decode('utf-8')
        }
    }
    
    return documento_seguro

def descifrar_reporte(documento_seguro, llave):
    """Verifica el tag de autenticidad y descifra los datos privados del ganadero."""
    chacha = ChaCha20Poly1305(llave)
    
    nonce = base64.b64decode(documento_seguro["datos_privacidad_ganadero"]["nonce"])
    ciphertext_con_tag = base64.b64decode(documento_seguro["datos_privacidad_ganadero"]["ciphertext_and_tag"])
    
    # decrypt() lanza InvalidTag si el ciphertext fue alterado (AEAD integrity check)
    datos_planos_bytes = chacha.decrypt(nonce, ciphertext_con_tag, associated_data=None)
    return json.loads(datos_planos_bytes.decode('utf-8'))

def main():
    print("📱 Iniciando simulación de la App Móvil...")
    
    # 1. El ganadero llena los datos
    datos_completos = simular_captura_app_movil()
    print(f"✅ Formulario capturado: Reporte {datos_completos['id_reporte']}")
    
    # 2. Obtenemos la llave de encriptación
    llave = generar_llave_maestra()
    
    # 3. Aplicamos la Criptografía (ChaCha20)
    print("🔒 Aplicando cifrado a nivel de campo (Field-Level Encryption)...")
    documento_nosql = cifrar_reporte(datos_completos, llave)
    
    # 4. Guardamos el resultado como lo vería la base de datos NoSQL
    # Detectamos la ruta para guardarlo en la carpeta correcta
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(base_dir, 'data', 'nosql')
    os.makedirs(out_dir, exist_ok=True)
    
    ruta_salida = os.path.join(out_dir, 'ejemplo_reporte_cifrado.json')
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(documento_nosql, f, indent=4, ensure_ascii=False)
        
    print(f"🚀 ¡Éxito! El documento seguro para NoSQL se ha guardado en:")
    print(f"   {ruta_salida}")
    
    print("\nVisualización de cómo llega a MongoDB:")
    print("-" * 50)
    print(json.dumps(documento_nosql, indent=2, ensure_ascii=False))
    print("-" * 50)
    
    # 5. Verificamos que el descifrado funciona correctamente (prueba de round-trip)
    print("\n🔓 Verificando descifrado (round-trip test)...")
    datos_recuperados = descifrar_reporte(documento_nosql, llave)
    assert datos_recuperados["nombre_ganadero"] == "Juan Pérez", "❌ ERROR: Datos no coinciden"
    print("✅ Datos descifrados correctamente. Tag de autenticidad verificado.")
    print(f"   Ganadero: {datos_recuperados['nombre_ganadero']} | Predio: {datos_recuperados['id_predio']}")

if __name__ == "__main__":
    main()
