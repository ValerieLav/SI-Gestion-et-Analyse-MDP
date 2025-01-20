import unittest
from backend.encryption import generate_key, encrypt_password, decrypt_password

class TestEncryption(unittest.TestCase):
    def test_generate_key(self):
        key = generate_key()
        self.assertIsNotNone(key)

    def test_encrypt_decrypt_password(self):
        key = generate_key()
        password = "mysecretpassword"
        encrypted_password = encrypt_password(key, password)
        decrypted_password = decrypt_password(key, encrypted_password)
        self.assertEqual(password, decrypted_password)

if __name__ == '__main__':
    unittest.main()