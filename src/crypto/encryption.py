def cifrar_cesar(texto, k):
    """
    Cifra un texto utilizando el cifrado César con un desplazamiento k.
    Conserva espacios y caracteres especiales de acuerdo al plan de delegación.
    """
    resultado = []
    for char in texto:
        if char.isalpha():
            # Letras mayúsculas
            if char.isupper():
                resultado.append(chr((ord(char) - 65 + k) % 26 + 65))
            # Letras minúsculas
            else:
                resultado.append(chr((ord(char) - 97 + k) % 26 + 97))
        else:
            # No es letra alfabética (puntuación, espacio, etc.), se conserva intacto
            resultado.append(char)
    return "".join(resultado)

def descifrar_cesar(texto, k):
    """
    Descifra un texto cifrado con César utilizando la función iterativamente pero con factor negativo.
    """
    return cifrar_cesar(texto, -k)

if __name__ == "__main__":
    print("--- Prueba de Criptografía (Miembro 1) ---")
    
    # Prueba estándar
    test_word = "Bachoco"
    cifrado = cifrar_cesar(test_word, 7)
    descifrado = descifrar_cesar(cifrado, 7)
    print(f"Original: {test_word} -> Cifrado: {cifrado} -> Descifrado: {descifrado}")
    
    assert descifrado == test_word, "Error en la bidireccionalidad de letras normales"
    
    # Manejo de caracteres especiales (Guard estipulado en la rúbrica)
    test_empresa = "S.A. DE C.V."
    cifrado_empresa = cifrar_cesar(test_empresa, 7)
    descifrado_empresa = descifrar_cesar(cifrado_empresa, 7)
    print(f"Especial: {test_empresa} -> Cifrado: {cifrado_empresa} -> Descifrado: {descifrado_empresa}")
    
    assert descifrado_empresa == test_empresa, "Error conservando caracteres especiales"
    
    print("\n✅ Todas las pruebas de validación pasaron (bidireccionalidad y no-alfabéticos)")
