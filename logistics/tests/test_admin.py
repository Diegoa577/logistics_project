"""
Tests for the Django admin modifications.
"""
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from logistics.models import Booking, Vehicle
from logistics.admin import BookingAdmin, VehicleAdmin
from datetime import date
from django.contrib.auth import get_user_model

class MockRequest:
    pass

class BookingAdminTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.create_superuser())
        self.site = AdminSite()
        self.admin = BookingAdmin(Booking, self.site)
        self.booking = Booking.objects.create(
            booking_number='B12345',
            loading_port='Port A',
            discharge_port='Port B',
            ship_arrival_date=date(2024, 8, 1),
            ship_departure_date=date(2024, 8, 5)
        )

    def create_superuser(self):
        User = get_user_model()
        return User.objects.create_superuser(username='admin', password='password', email='admin@example.com')

    def test_booking_admin_str(self):
        self.assertEqual(str(self.booking), 'B12345')

    def test_booking_admin_list_display(self):
        self.assertEqual(self.admin.list_display, ('booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date'))

    def test_booking_admin_changelist_view(self):
        response = self.client.get('/admin/logistics/booking/')
        self.assertEqual(response.status_code, 200)

    def test_booking_admin_change_view(self):
        response = self.client.get(f'/admin/logistics/booking/{self.booking.id}/change/')
        self.assertEqual(response.status_code, 200)


class VehicleAdminTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.create_superuser())
        self.site = AdminSite()
        self.admin = VehicleAdmin(Vehicle, self.site)
        self.booking = Booking.objects.create(
            booking_number='B12345',
            loading_port='Port A',
            discharge_port='Port B',
            ship_arrival_date=date(2024, 8, 1),
            ship_departure_date=date(2024, 8, 5)
        )
        self.vehicle = Vehicle.objects.create(
            vin='1HGCM82633A123456',
            make='Honda',
            model='Accord',
            weight=1500,
            booking=self.booking
        )

    def create_superuser(self):
        User = get_user_model()
        return User.objects.create_superuser(username='admin', password='password', email='admin@example.com')

    def test_vehicle_admin_str(self):
        self.assertEqual(str(self.vehicle), '1HGCM82633A123456')

    def test_vehicle_admin_list_display(self):
        self.assertEqual(self.admin.list_display, ('vin', 'make', 'model', 'weight', 'booking'))

    def test_vehicle_admin_changelist_view(self):
        response = self.client.get('/admin/logistics/vehicle/')
        self.assertEqual(response.status_code, 200)

    def test_vehicle_admin_change_view(self):
        response = self.client.get(f'/admin/logistics/vehicle/{self.vehicle.id}/change/')
        self.assertEqual(response.status_code, 200)
