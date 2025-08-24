from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.businesses.models import Business
from apps.appointments.models import Service, Appointment
from datetime import date, time


User = get_user_model()

class ServiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="owner@test.com", password="12345")
        self.business = Business.objects.create(
            owner=self.user,
            name="Clinic",
            description="Medical Clinic",
        )
        self.service = Service.objects.create(
            business=self.business,
            name="Consultation",
            description="General health check",
            price=200000,
            duration=30,
            capacity=2
        )

    def test_service_str(self):
        """__str__ returns 'service name (business name)'"""
        self.assertEqual(str(self.service), "Consultation (Clinic)")

    def test_service_business_relation(self):
        self.assertEqual(self.service.business, self.business)

    def test_service_price_and_capacity(self):
        self.assertEqual(self.service.price, 200000)
        self.assertEqual(self.service.capacity, 2)


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="patient@test.com", password="12345")
        self.owner = User.objects.create_user(email="owner@test.com", password="12345")

        self.business = Business.objects.create(owner=self.owner, name="Clinic")
        self.service = Service.objects.create(
            business=self.business,
            name="Consultation",
            price=150000,
            duration=45,
            capacity=1
        )

        self.appointment = Appointment.objects.create(
            service=self.service,
            user=self.user,
            date=date(2025, 8, 20),
            time=time(14, 0)
        )

    def test_appointment_str(self):
        expected_str = f"{self.user.email} - {self.service.name} on {self.appointment.date} at {self.appointment.time}"
        self.assertEqual(str(self.appointment), expected_str)

    def test_appointment_default_status(self):
        """Status should be 'pending' by default"""
        self.assertEqual(self.appointment.status, "pending")

    def test_appointment_can_change_status(self):
        """Appointment status can be updated"""
        self.appointment.status = "confirmed"
        self.appointment.save()
        self.assertEqual(self.appointment.status, "confirmed")

    def test_appointment_service_and_business_relation(self):
        self.assertEqual(self.appointment.service, self.service)
        self.assertEqual(self.appointment.service.business, self.business)