import datetime
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_root_ca():
    # Fix 1: Automatically create directories to prevent FileNotFoundError
    folders = ["storage/keys", "storage/certs"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Created missing directory: {folder}")

    # Generate CA Private Key
    ca_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Define CA Identity
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"HRMS Trust CA"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"hrms-root-ca.local"),
    ])

    # Fix 2: Use timezone-aware UTC datetime to remove DeprecationWarning
    now = datetime.datetime.now(datetime.timezone.utc)

    # Build the Certificate
    root_cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        ca_private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        now
    ).not_valid_after(
        now + datetime.timedelta(days=3650)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    ).sign(ca_private_key, hashes.SHA256())

    # Save to files
    with open("storage/keys/ca_private_key.pem", "wb") as f:
        f.write(ca_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    with open("storage/certs/root_ca.crt", "wb") as f:
        f.write(root_cert.public_bytes(serialization.Encoding.PEM))

    print("✅ Root CA and Certificate generated successfully in /storage folder.")

if __name__ == "__main__":
    generate_root_ca()


    ghjm hjmk