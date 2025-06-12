import sys
import os
import json
import base64
import getpass
from inputimeout import inputimeout, TimeoutOccurred

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- Configuration ---
KDF_ITERATIONS = 480000
SALT_SIZE = 16
TIMEOUT_SECONDS = 300  # 5 minutes


def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a Fernet key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def load_store(filepath: str) -> (dict, str):
    """Loads and decrypts an existing password store."""
    master_password = getpass.getpass("Enter master password: ")

    with open(filepath, "r") as f:
        data = json.load(f)

    salt = base64.b64decode(data["salt"])
    encrypted_data = base64.b64decode(data["encrypted_data"])

    key = derive_key(master_password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        passwords = json.loads(decrypted_data)
        print("Vault unlocked successfully.")
        return passwords, master_password
    except InvalidToken:
        print("Error: Invalid master password or corrupted file.")
        sys.exit(1)


def print_help(): #print nice disply of help commands

    print("\nAvailable commands:")
    print("  get <service>              - Get password for a service")
    print("  set <service> <user> <pass>- Add/update a password")
    print("  del <service>              - Delete a password")
    print("  list                       - List all services")
    print("  help                       - Show this help message")
    print("  exit                       - Save and exit the vault\n")



def create_new_store() -> tuple[dict, str]: #create master password, return dict with master password
    print("NO current vault, creating new one....")
    master_password = getpass.getpass("Enter NEW(!) password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if master_password != confirm_password:
        print("You entered a different confirmation password/phrase")
        sys.exit(1)

    print("New vault created :)")
    return {}, master_password


def save_store(filepath: str, passwords: dict, master_password: str): #encrypt and save pw to file
    
    salt = os.urandom(SALT_SIZE)
    key = derive_key(master_password, salt)
    fernet = Fernet(key)

    passwords_bytes = json.dumps(passwords).encode()
    encrypted_data = fernet.encrypt(passwords_bytes)

    file_content = {
        "salt": base64.b64encode(salt).decode("utf-8"),
        "encrypted_data": base64.b64encode(encrypted_data).decode("utf-8"),
    }

    temp_filepath = filepath + ".tmp"
    with open(temp_filepath, "w") as f:
        json.dump(file_content, f, indent=2)

    os.rename(temp_filepath, filepath)
    print(f"Vault saved and locked at '{filepath}'.")
