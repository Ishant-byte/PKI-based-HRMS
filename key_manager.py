import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_employee_keys(employee_name):
    # 1. Create directory if missing
    if not os.path.exists("storage/keys"):
        os.makedirs("storage/keys")

    # 2. Generate RSA Private Key (Requirement 4)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # 3. Save Private Key locally (Simulating secure endpoint storage)
    key_filename = f"storage/keys/{employee_name}_private.pem"
    with open(key_filename, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(), # In prod, use a password here
        ))

    # 4. Create a Certificate Signing Request (CSR) (Requirement 1)
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"HRMS Employee"),
        x509.NameAttribute(NameOID.COMMON_NAME, employee_name),
    ])).sign(private_key, hashes.SHA256()) # Sign the request with the new key

    # 5. Save the CSR to be "sent" to the CA
    csr_filename = f"storage/keys/{employee_name}.csr"
    with open(csr_filename, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    print(f"✅ Keys and CSR generated for: {employee_name}")
    print(f"📍 Private Key: {key_filename}")
    print(f"📍 CSR: {csr_filename}")

if __name__ == "__main__":
    # Test with a dummy name
    generate_employee_keys("Ishant_G")