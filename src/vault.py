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
