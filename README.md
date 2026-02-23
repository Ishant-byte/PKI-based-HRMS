# SajiloHRMS — PKI-secured HRMS (Tkinter + MongoDB)
# --Developer: ISHANT
This is a **local-hosted** HRMS-style application built to demonstrate **PKI-based cryptography**:
- Certificate-based authentication (challenge-response)
- Password + OTP (2FA) login
- Key/certificate issuance + revocation (CRL)
- Document signing + verification with signature bundles
- End-to-end encrypted 1:1 chat with disappearing messages (TTL)
- Field-level encryption for sensitive data at rest (AES-256-GCM)
- Admin security/audit logs + user self-logs
- Tkinter cyberpunk UI with separate Admin/User portals + animations

## 1) Prerequisites
- Python 3.10+
- MongoDB running locally (required)
- (Recommended) create and activate a venv

## 2) Quick setup (Windows PowerShell)
From the project root:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
scripts\bootstrap.ps1
```

## 3) Install dependencies (manual)
```bash
pip install -r requirements.txt
```

## 4) Start MongoDB (required)
Default connection: `mongodb://localhost:27017` (DB name: `sajilohr`)

If MongoDB is **not** running, the server will refuse to start and the client will not operate.

## 5) Start the server
```bash
python -m server.app
```

Server will:
- Connect to MongoDB
- Create indexes
- Create a local Root CA if missing in `pki/ca/`
- Seed a default admin account if missing:
  - username: `admin@sajilohr.local`
  - password: `Admin@123`
  - role: Admin
  - (A certificate + PKCS#12 keystore will be generated on first run)

### OTP behavior
During login, the OTP is shown in a **client popup** for demo convenience.
It is also printed to the **server terminal** as a fallback.

## 6) Start the client
```bash
python -m client.main
```

Choose **Admin Portal** or **Employee Portal** on the landing screen.

## 7) Registration (public)
From the Login screen in either portal:
- Click **Register**
- Fill your details (strong password policy is enforced)
- After registration, your keystore is saved under: `pki/users/<username>/keystore.p12`

Note: Admin accounts are privileged. This build allows Admin self-registration for coursework/demo convenience.

## 8) Document signing & verification
Employee portal → Documents:
- Sign: browse file → sign → export bundle as ZIP
- Verify: upload file + bundle ZIP → verify signature, hash, certificate chain, CRL

## 9) Chat (E2E + disappearing)
Employee/Admin → Chat:
- Select a user/admin
- Messages are encrypted end-to-end and stored as ciphertext.
- Disappearing messages use MongoDB TTL; you can choose expiry when sending.

## 10) Configuration
Environment variables (optional):
- `MONGO_URI` (default `mongodb://localhost:27017`)
- `MONGO_DB` (default `sajilohr`)
- `JWT_SECRET` (default generated at runtime; for consistent tokens set a value)
- `SERVER_KEK_PASSPHRASE` (default `change-me`) used to encrypt the server KEK file.

## 11) Tests
```bash
pytest -q
```

## Security note (local demo)
This project is built for **academic assessment** and local-hosted demonstration.
For production, secrets storage, certificate lifecycle, and deployment hardening would need upgrades.
