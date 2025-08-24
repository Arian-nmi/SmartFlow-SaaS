from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.reports.models import Report


User = get_user_model()

class ReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="12345")

    def test_report_creation_defaults(self):
        """Report should be created with status=pending by default"""
        report = Report.objects.create(
            requested_by=self.user,
            report_type=Report.TYPE_APPOINTMENTS,
            filters={"date_from": "2025-01-01", "date_to": "2025-01-31"}
        )
        self.assertEqual(report.status, Report.STATUS_PENDING)
        self.assertEqual(report.report_type, "appointments")
        self.assertEqual(report.filters["date_from"], "2025-01-01")
        self.assertFalse(report.file_path)

    def test_report_str(self):
        report = Report.objects.create(
            requested_by=self.user,
            report_type=Report.TYPE_BUSINESSES,
        )
        self.assertEqual(str(report), "businesses (pending)")

    def test_report_change_status(self):
        report = Report.objects.create(
            requested_by=self.user,
            report_type=Report.TYPE_APPOINTMENTS,
        )
        report.status = Report.STATUS_READY
        report.save()
        self.assertEqual(report.status, Report.STATUS_READY)

    def test_report_related_to_user(self):
        report = Report.objects.create(
            requested_by=self.user,
            report_type=Report.TYPE_BUSINESSES,
        )
        self.assertEqual(report.requested_by, self.user)
        self.assertEqual(self.user.reports.first(), report)

    def test_ordering_meta_option(self):
        first = Report.objects.create(requested_by=self.user, report_type=Report.TYPE_APPOINTMENTS)
        second = Report.objects.create(requested_by=self.user, report_type=Report.TYPE_BUSINESSES)
        reports = Report.objects.all()
        self.assertEqual(reports[0], second)
        self.assertEqual(reports[1], first)