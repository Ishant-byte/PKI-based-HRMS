import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def sign_and_encrypt_document(employee_name, document_path, manager_cert_path):
    # 1. Load Employee Private Key for Signing
    with open(f"storage/keys/{employee_name}_private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # 2. Load Manager Public Key for Encryption (Hybrid)
    with open(manager_cert_path, "rb") as f:
        manager_cert = x509.load_pem_x509_certificate(f.read())
        manager_public_key = manager_cert.public_key()

    # 3. Read the Document
    with open(document_path, "rb") as f:
        doc_data = f.read()

    # --- DIGITAL SIGNATURE (Requirement 2) ---
    signature = private_key.sign(
        doc_data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    # --- AES ENCRYPTION (Requirement 3) ---
    aes_key = os.urandom(32) # 256-bit key
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(doc_data) + encryptor.finalize()

    # --- HYBRID KEY WRAP (Requirement 3) ---
    encrypted_aes_key = manager_public_key.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # 4. Save the bundle
    output_base = f"storage/documents/{employee_name}_contract"
    if not os.path.exists("storage/documents"): os.makedirs("storage/documents")
    
    with open(f"{output_base}.enc", "wb") as f: f.write(ciphertext)
    with open(f"{output_base}.sig", "wb") as f: f.write(signature)
    with open(f"{output_base}.key", "wb") as f: f.write(encrypted_aes_key)
    with open(f"{output_base}.iv", "wb") as f: f.write(iv)

    print(f"✅ Document signed and encrypted for {employee_name}.")