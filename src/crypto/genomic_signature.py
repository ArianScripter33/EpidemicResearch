import os
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

KEYS_DIR = os.path.join(os.path.dirname(__file__), "keys")

def generate_and_save_keys(key_name: str = "veterinario_cpa") -> tuple:
    """
    Genera un par de llaves RSA de 2048 bits y las guarda en el directorio local de llaves.
    """
    os.makedirs(KEYS_DIR, exist_ok=True)
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    public_key = private_key.public_key()
    
    # Serializar y guardar llave privada
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption() # Sin contraseña para simplificar el desarrollo
    )
    
    private_path = os.path.join(KEYS_DIR, f"{key_name}_private.pem")
    with open(private_path, "wb") as f:
        f.write(private_pem)
        
    # Serializar y guardar llave pública
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    public_path = os.path.join(KEYS_DIR, f"{key_name}_public.pem")
    with open(public_path, "wb") as f:
        f.write(public_pem)
        
    return private_key, public_key

def load_private_key(key_name: str = "veterinario_cpa"):
    """Carga la llave privada RSA desde el archivo local PEM."""
    private_path = os.path.join(KEYS_DIR, f"{key_name}_private.pem")
    if not os.path.exists(private_path):
        generate_and_save_keys(key_name)
        
    with open(private_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    return private_key

def load_public_key(key_name: str = "veterinario_cpa"):
    """Carga la llave pública RSA desde el archivo local PEM."""
    public_path = os.path.join(KEYS_DIR, f"{key_name}_public.pem")
    if not os.path.exists(public_path):
        generate_and_save_keys(key_name)
        
    with open(public_path, "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read()
        )
    return public_key

def sign_genomic_report(report_data: dict, key_name: str = "veterinario_cpa") -> str:
    """
    Calcula el hash SHA-256 de un reporte genómico en formato dict y lo firma digitalmente con RSA.
    Retorna la firma codificada en hexadecimal.
    """
    private_key = load_private_key(key_name)
    
    # Serializar el diccionario a una cadena JSON estandarizada (con claves ordenadas)
    serialized_data = json.dumps(report_data, sort_keys=True).encode('utf-8')
    
    # Firmar el payload usando padding PSS
    signature = private_key.sign(
        serialized_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    return signature.hex()

def verify_genomic_signature(report_data: dict, signature_hex: str, key_name: str = "veterinario_cpa") -> bool:
    """
    Verifica si una firma digital (hexadecimal) corresponde al reporte genómico provisto
    usando la llave pública RSA correspondiente.
    """
    public_key = load_public_key(key_name)
    
    # Serializar el diccionario a una cadena JSON estandarizada (con claves ordenadas)
    serialized_data = json.dumps(report_data, sort_keys=True).encode('utf-8')
    
    try:
        signature = bytes.fromhex(signature_hex)
        public_key.verify(
            signature,
            serialized_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except (InvalidSignature, ValueError):
        return False
