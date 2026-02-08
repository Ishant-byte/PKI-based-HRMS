import os
from core.ca_authority import generate_root_ca
from client.key_manager import generate_employee_keys
from core.registration_handler import sign_employee_csr
from client.signer import sign_and_encrypt_document
from core.verifier import verify_and_decrypt

# 1. Setup Environment
employee = "Ishant_G"
doc_path = "storage/documents/contract.txt"

if not os.path.exists("storage/documents"):
    os.makedirs("storage/documents")

# Create a dummy contract file
with open(doc_path, "w") as f:
    f.write("This is a highly sensitive HR contract for Ishant_G. Confidentiality is key!")

print("--- 🚀 Starting PKI Workflow ---")

# 2. CA Setup (Central Manager)
generate_root_ca()

# 3. Employee Key Gen (Endpoint)
generate_employee_keys(employee)

# 4. Certificate Issuance (Registration)
sign_employee_csr(employee)

# 5. Sign and Encrypt (The "Action")
# We use the Root CA's cert as the 'Manager Cert' for this demo
sign_and_encrypt_document(employee, doc_path, "storage/certs/root_ca.crt")

# 6. Verify and Decrypt (The "Audit")
verify_and_decrypt(employee, "HR_Manager")

print("--- ✅ Workflow Complete ---")