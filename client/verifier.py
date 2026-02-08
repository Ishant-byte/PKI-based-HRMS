import os
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidSignature

def verify_and_decrypt(employee_name, manager_name):
    base_path = f"storage/documents/{employee_name}_contract"
    
    # 1. Load Employee's Certificate to get their Public Key for verification
    with open(f"storage/certs/{employee_name}.crt", "rb") as f:
        emp_cert = x509.load_pem_x509_certificate(f.read())
        emp_public_key = emp_cert.public_key()

    # 2. Load Manager's Private Key for Decryption
    # In our test, manager is the Root CA
    with open(f"storage/keys/ca_private_key.pem", "rb") as f:
        mgr_private_key = serialization.load_pem_private_key(f.read(), password=None)

    # 3. Load the components from storage
    with open(f"{base_path}.enc", "rb") as f: ciphertext = f.read()
    with open(f"{base_path}.sig", "rb") as f: signature = f.read()
    with open(f"{base_path}.key", "rb") as f: encrypted_aes_key = f.read()
    with open(f"{base_path}.iv", "rb") as f: iv = f.read()

    # --- HYBRID DECRYPTION (Requirement 3) ---
    # Decrypt the AES key using Manager's RSA Private Key
    aes_key = mgr_private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # Decrypt the document using the AES key
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_doc = decryptor.update(ciphertext) + decryptor.finalize()

    # --- SIGNATURE VERIFICATION (Requirement 2) ---
    try:
        emp_public_key.verify(
            signature,
            decrypted_doc,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print("✅ VERIFICATION SUCCESS: Signature is valid. Document integrity confirmed.")
        print(f"📄 Decrypted Content: {decrypted_doc.decode('utf-8')}")
        return decrypted_doc
    except InvalidSignature:
        print("❌ VERIFICATION FAILED: Signature is invalid! The document may be tampered.")
        return None

if __name__ == "__main__":
    verify_and_decrypt("Ishant_G", "HR_Manager")