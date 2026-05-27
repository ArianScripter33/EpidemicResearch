import os
import base64
import bcrypt
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from src.crypto.genomic_signature import load_private_key, load_public_key

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt con 12 rounds de sal (como se especifica en el 3er avance).
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """
    Verifica una contraseña contra su hash de bcrypt.
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def encrypt_pii(text: str, key_name: str = "veterinario_cpa") -> str:
    """
    Encripta datos personales identificables (PII) usando la llave pública RSA
    y un esquema de padding OAEP con SHA-256. Retorna la cadena en Base64.
    """
    if not text:
        return ""
    public_key = load_public_key(key_name)
    cipher_bytes = public_key.encrypt(
        text.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(cipher_bytes).decode('utf-8')

def decrypt_pii(cipher_text_b64: str, key_name: str = "veterinario_cpa") -> str:
    """
    Desencripta un dato personal identificable (PII) usando la llave privada RSA
    y padding OAEP con SHA-256.
    """
    if not cipher_text_b64:
        return ""
    private_key = load_private_key(key_name)
    cipher_bytes = base64.b64decode(cipher_text_b64.encode('utf-8'))
    plain_bytes = private_key.decrypt(
        cipher_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plain_bytes.decode('utf-8')

if __name__ == "__main__":
    print("--- Prueba de Criptografía Profesional (Auditada) ---")
    
    # 1. Prueba de Contraseña (bcrypt 12 rounds)
    raw_pass = "GanadoSaludable2026!"
    hashed_pass = hash_password(raw_pass)
    print(f"\n🔑 Bcrypt Hash (12 rounds): {hashed_pass}")
    
    # Verificaciones
    assert verify_password(raw_pass, hashed_pass) is True, "Error: La contraseña válida debería pasar"
    assert verify_password("incorrect_pass", hashed_pass) is False, "Error: Contraseña incorrecta debería fallar"
    print("✅ Bcrypt: Contraseñas encriptadas y verificadas con éxito.")
    
    # 2. Prueba de Datos Personales (PII - RSA Field Level Encryption)
    ganadero_nombre = "Don Aurelio Gómez Estrada"
    rfc_curp = "GOEA670415MXX"
    email = "aurelio.gomez@rancho_la_loma.mx"
    
    print(f"\n🔒 Datos Originales PII:")
    print(f"   Nombre: {ganadero_nombre}")
    print(f"   RFC: {rfc_curp}")
    print(f"   Email: {email}")
    
    enc_nombre = encrypt_pii(ganadero_nombre)
    enc_rfc = encrypt_pii(rfc_curp)
    enc_email = encrypt_pii(email)
    
    print(f"\n🔐 Datos Encriptados (RSA Base64):")
    print(f"   Nombre: {enc_nombre[:30]}...")
    print(f"   RFC: {enc_rfc[:30]}...")
    print(f"   Email: {enc_email[:30]}...")
    
    dec_nombre = decrypt_pii(enc_nombre)
    dec_rfc = decrypt_pii(enc_rfc)
    dec_email = decrypt_pii(enc_email)
    
    print(f"\n🔓 Datos Desencriptados:")
    print(f"   Nombre: {dec_nombre}")
    print(f"   RFC: {dec_rfc}")
    print(f"   Email: {dec_email}")
    
    assert dec_nombre == ganadero_nombre, "Error en desencripción de nombre"
    assert dec_rfc == rfc_curp, "Error en desencripción de RFC"
    assert dec_email == email, "Error en desencripción de email"
    
    print("\n✅ RSA: Cifrado y descifrado asimétrico asertados correctamente.")
