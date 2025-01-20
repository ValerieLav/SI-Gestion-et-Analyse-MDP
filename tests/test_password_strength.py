import unittest
from backend.password_strength import generate_password, is_secure_password, is_password_safe

class TestPasswordStrength(unittest.TestCase):
    def test_generate_password(self):
        password = generate_password()
        self.assertTrue(len(password) >= 8)

    def test_is_secure_password(self):
        self.assertTrue(is_secure_password("StrongPass1!"))
        self.assertFalse(is_secure_password("weak"))

    def test_is_password_safe(self):
        self.assertTrue(is_password_safe("UniquePass1!"))
        self.assertFalse(is_password_safe("password123"))

if __name__ == '__main__':
    unittest.main()