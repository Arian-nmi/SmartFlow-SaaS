from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.businesses.models import Business


User = get_user_model()

class BusinessModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="owner@test.com", password="12345")
        self.business = Business.objects.create(
            owner=self.user,
            name="Test Business",
            description="A sample test business",
            address="Tehran, Iran",
            phone="09120000000"
        )

    def test_business_str(self):
        """__str__ should return the name"""
        self.assertEqual(str(self.business), "Test Business")

    def test_business_owner_relation(self):
        """Business should be linked to the correct owner"""
        self.assertEqual(self.business.owner.email, "owner@test.com")

    def test_business_optional_fields(self):
        """Optional fields (description, address, phone) should save correctly"""
        self.assertEqual(self.business.description, "A sample test business")
        self.assertEqual(self.business.address, "Tehran, Iran")
        self.assertEqual(self.business.phone, "09120000000")

    def test_business_can_be_created_with_minimum_fields(self):
        """A Business can be created even if description, address, phone are blank"""
        biz = Business.objects.create(owner=self.user, name="Minimal Biz")
        self.assertEqual(biz.name, "Minimal Biz")
        self.assertEqual(biz.description, "")
        self.assertEqual(biz.address, "")
        self.assertEqual(biz.phone, "")

    def test_business_created_and_updated_at(self):
        """created_at and updated_at should be auto populated"""
        self.assertIsNotNone(self.business.created_at)
        self.assertIsNotNone(self.business.updated_at)