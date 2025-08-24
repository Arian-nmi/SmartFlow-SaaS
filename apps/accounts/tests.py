from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserModelTest(TestCase):
    def test_create_user_with_email(self):
        """should create a user with email and password"""
        user = User.objects.create_user(email="test@example.com", password="pass123", full_name="jerald")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("pass123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_user_without_email_raises_error(self):
        """creating user without email should raise ValueError"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="pass123")

    def test_create_superuser(self):
        """should create superuser with is_staff=True and is_superuser=True"""
        superuser = User.objects.create_superuser(email="admin@test.com", password="adminpass")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.email, "admin@test.com")

    def test_password_unusable_if_not_given(self):
        """if no password is provided, user must have unusable password"""
        user = User.objects.create_user(email="nopass@test.com")
        self.assertFalse(user.has_usable_password())

    def test_str_returns_email(self):
        user = User.objects.create_user(email="str@test.com", password="test123")
        self.assertEqual(str(user), "str@test.com")

    def test_str_returns_phone_if_no_email(self):
        user = User.objects.create(phone_number="09123456789")
        self.assertEqual(str(user), "09123456789")

    def test_str_returns_fallback_if_no_email_or_phone(self):
        user = User.objects.create()
        expected = f"User {user.id}"
        self.assertEqual(str(user), expected)