import unittest
from backend.storage import store_password, retrieve_password

class TestStorage(unittest.TestCase):
    def test_store_and_retrieve_password(self):
        # Utiliser un mot de passe chiffré de type bytes
        encrypted_password = b"encrypted_password"
        store_password("site", "username", encrypted_password, "test_passwords.json")
        retrieved_password = retrieve_password("site", "username", "test_passwords.json")
        self.assertEqual(retrieved_password, encrypted_password.decode())

if __name__ == '__main__':
    unittest.main()