import tkinter as tk
from tkinter import messagebox, filedialog
from client.signer import sign_and_encrypt_document
from core.verifier import verify_and_decrypt

class HRMS_App:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure HRMS - PKI Dashboard")
        self.root.geometry("500x400")

        # UI Components
        tk.Label(root, text="HRMS Cryptographic Tool", font=("Arial", 16, "bold")).pack(pady=10)

        # Employee Section
        self.emp_frame = tk.LabelFrame(root, text="Employee: Sign Document", padx=10, pady=10)
        self.emp_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Button(self.emp_frame, text="Select & Sign Contract", command=self.handle_sign).pack()

        # Manager Section
        self.mgr_frame = tk.LabelFrame(root, text="Manager: Verify & Decrypt", padx=10, pady=10)
        self.mgr_frame.pack(fill="x", padx=20, pady=5)
        
        self.emp_name_entry = tk.Entry(self.mgr_frame)
        self.emp_name_entry.insert(0, "Ishant_G")
        self.emp_name_entry.pack(side="left", padx=5)
        
        tk.Button(self.mgr_frame, text="Verify Signature", command=self.handle_verify).pack(side="left")

    def handle_sign(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                # Using the demo logic
                sign_and_encrypt_document("Ishant_G", file_path, "storage/certs/root_ca.crt")
                messagebox.showinfo("Success", "Document Signed and Encrypted!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def handle_verify(self):
        name = self.emp_name_entry.get()
        result = verify_and_decrypt(name, "HR_Manager")
        if result:
            messagebox.showinfo("Audit Pass", f"Integrity Verified!\n\nContent: {result.decode()}")
        else:
            messagebox.showerror("Audit Fail", "Signature Invalid or Tampered!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HRMS_App(root)
    root.mainloop()