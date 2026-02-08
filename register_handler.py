import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization

def sign_employee_csr(employee_name):
    # 1. Load the Root CA Certificate and Private Key
    with open("storage/certs/root_ca.crt", "rb") as f:
        ca_cert = x509.load_pem_x509_certificate(f.read())
    
    with open("storage/keys/ca_private_key.pem", "rb") as f:
        ca_key = serialization.load_pem_private_key(f.read(), password=None)

    # 2. Load the Employee's CSR
    csr_path = f"storage/keys/{employee_name}.csr"
    with open(csr_path, "rb") as f:
        csr = x509.load_pem_x509_csr(f.read())

    # 3. Verify CSR signature (Requirement 2: Integrity check)
    if not csr.is_signature_valid:
        print(f"❌ Error: CSR signature for {employee_name} is invalid!")
        return

    # 4. Create the X.509 Certificate (Requirement 1: Authentication)
    now = datetime.datetime.now(datetime.timezone.utc)
    employee_cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        now
    ).not_valid_after(
        now + datetime.timedelta(days=365) # Valid for 1 year
    ).sign(ca_key, hashes.SHA256()) # Signed by CA's Private Key

    # 5. Save the final certificate to the Trust Indexer (storage/certs)
    cert_filename = f"storage/certs/{employee_name}.crt"
    with open(cert_filename, "wb") as f:
        f.write(employee_cert.public_bytes(serialization.Encoding.PEM))

    print(f"✅ Certificate issued for: {employee_name}")
    print(f"📍 Saved to: {cert_filename}")

if __name__ == "__main__":
    sign_employee_csr("Ishant_G")