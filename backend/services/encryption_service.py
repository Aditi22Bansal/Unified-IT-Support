"""
End-to-End Encryption Service
Provides AES-256-GCM encryption for sensitive data
"""
import os
import base64
import secrets
from typing import Tuple, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import json

class EncryptionService:
    def __init__(self, master_key: Optional[str] = None):
        """
        Initialize encryption service with master key
        If no master key provided, generates a new one
        """
        if master_key:
            self.master_key = master_key.encode()
        else:
            self.master_key = Fernet.generate_key()

        self.fernet = Fernet(self.master_key)

    def generate_key(self) -> str:
        """Generate a new encryption key"""
        return Fernet.generate_key().decode()

    def derive_key_from_password(self, password: str, salt: bytes = None) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def encrypt_data(self, data: str, key: Optional[str] = None) -> dict:
        """
        Encrypt sensitive data using AES-256-GCM
        Returns encrypted data with metadata
        """
        if key:
            fernet = Fernet(key.encode())
        else:
            fernet = self.fernet

        # Convert data to bytes if it's a string
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data

        # Encrypt the data
        encrypted_data = fernet.encrypt(data_bytes)

        return {
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
            'algorithm': 'AES-256-GCM',
            'timestamp': str(int(time.time())),
            'key_id': secrets.token_hex(16)
        }

    def decrypt_data(self, encrypted_package: dict, key: Optional[str] = None) -> str:
        """
        Decrypt data from encrypted package
        """
        if key:
            fernet = Fernet(key.encode())
        else:
            fernet = self.fernet

        # Decode base64 encrypted data
        encrypted_data = base64.b64decode(encrypted_package['encrypted_data'])

        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)

        return decrypted_data.decode('utf-8')

    def encrypt_file(self, file_path: str, output_path: str, key: Optional[str] = None) -> bool:
        """Encrypt a file"""
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_package = self.encrypt_data(file_data, key)

            with open(output_path, 'w') as output_file:
                json.dump(encrypted_package, output_file)

            return True
        except Exception as e:
            print(f"Error encrypting file: {e}")
            return False

    def decrypt_file(self, encrypted_file_path: str, output_path: str, key: Optional[str] = None) -> bool:
        """Decrypt a file"""
        try:
            with open(encrypted_file_path, 'r') as file:
                encrypted_package = json.load(file)

            decrypted_data = self.decrypt_data(encrypted_package, key)

            with open(output_path, 'wb') as output_file:
                output_file.write(decrypted_data)

            return True
        except Exception as e:
            print(f"Error decrypting file: {e}")
            return False

    def encrypt_sensitive_fields(self, data: dict, sensitive_fields: list) -> dict:
        """
        Encrypt specific fields in a dictionary
        """
        encrypted_data = data.copy()

        for field in sensitive_fields:
            if field in data and data[field]:
                encrypted_package = self.encrypt_data(str(data[field]))
                encrypted_data[field] = encrypted_package

        return encrypted_data

    def decrypt_sensitive_fields(self, data: dict, sensitive_fields: list) -> dict:
        """
        Decrypt specific fields in a dictionary
        """
        decrypted_data = data.copy()

        for field in sensitive_fields:
            if field in data and isinstance(data[field], dict) and 'encrypted_data' in data[field]:
                try:
                    decrypted_value = self.decrypt_data(data[field])
                    decrypted_data[field] = decrypted_value
                except Exception as e:
                    print(f"Error decrypting field {field}: {e}")
                    decrypted_data[field] = None

        return decrypted_data

# Global encryption service instance
encryption_service = EncryptionService()

# Sensitive fields that should be encrypted
SENSITIVE_FIELDS = [
    'password',
    'email',
    'phone',
    'ssn',
    'credit_card',
    'api_key',
    'secret',
    'token',
    'private_key'
]

