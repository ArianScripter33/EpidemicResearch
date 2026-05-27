from src.crypto.genomic_signature import (
    generate_and_save_keys,
    sign_genomic_report,
    verify_genomic_signature
)

def test_genomic_signing_lifecycle():
    # 1. Generar llaves para la prueba
    generate_and_save_keys("test_vet")
    
    # 2. Crear payload de secuenciación genómica de prueba (Salmonella con BLEE)
    report = {
        "establecimiento": "Rastro Municipal de Veracruz, Lote 45",
        "fecha_analisis": "2026-05-21T15:30:00Z",
        "patogeno": "Salmonella enterica serovar Typhimurium",
        "genes_resistencia_detectados": ["blaCTX-M-15", "blaTEM-1", "tetA"],
        "concentracion_inhibitoria_mic": {
            "ampicilina": ">32 ug/mL",
            "ceftriaxona": "16 ug/mL",
            "tetraciclina": ">64 ug/mL"
        },
        "score_ram_calculado": 0.94
    }
    
    # 3. Firmar el reporte
    firma_hex = sign_genomic_report(report, "test_vet")
    assert isinstance(firma_hex, str)
    assert len(firma_hex) > 0
    print(f"Firma digital generada con éxito: {firma_hex[:20]}...")
    
    # 4. Verificar firma válida
    es_valida = verify_genomic_signature(report, firma_hex, "test_vet")
    assert es_valida is True
    
    # 5. Intentar alterar datos (simulando ataque hacker)
    report_alterado = report.copy()
    report_alterado["score_ram_calculado"] = 0.0  # El atacante falsifica el riesgo genómico para pasar la auditoría
    
    # Verificar que la firma es rechazada
    es_valida_alterado = verify_genomic_signature(report_alterado, firma_hex, "test_vet")
    assert es_valida_alterado is False
    print("La firma digital detectó y bloqueó la alteración de datos genómicos con éxito.")
    
    # 6. Intentar verificar con firma corrupta
    firma_corrupta_hex = firma_hex[:-4] + "0000"
    es_valida_corrupta = verify_genomic_signature(report, firma_corrupta_hex, "test_vet")
    assert es_valida_corrupta is False
    
    print("¡Todos los assertions criptográficos pasaron correctamente!")

if __name__ == "__main__":
    test_genomic_signing_lifecycle()
