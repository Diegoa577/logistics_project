"""
Tests for models.
"""
from django.test import TestCase
from logistics.models import Booking, Vehicle
from datetime import date

class BookingModelTest(TestCase):

    def setUp(self):
        self.booking = Booking.objects.create(
            booking_number='B12345',
            loading_port='Port A',
            discharge_port='Port B',
            ship_arrival_date=date(2024, 8, 1),
            ship_departure_date=date(2024, 8, 5)
        )

    def test_booking_creation(self):
        self.assertIsInstance(self.booking, Booking)
        self.assertEqual(self.booking.booking_number, 'B12345')
        self.assertEqual(self.booking.loading_port, 'Port A')
        self.assertEqual(self.booking.discharge_port, 'Port B')
        self.assertEqual(self.booking.ship_arrival_date, date(2024, 8, 1))
        self.assertEqual(self.booking.ship_departure_date, date(2024, 8, 5))

    def test_booking_str(self):
        self.assertEqual(str(self.booking), 'B12345')


class VehicleModelTest(TestCase):

    def setUp(self):
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

    def test_vehicle_creation(self):
        self.assertIsInstance(self.vehicle, Vehicle)
        self.assertEqual(self.vehicle.vin, '1HGCM82633A123456')
        self.assertEqual(self.vehicle.make, 'Honda')
        self.assertEqual(self.vehicle.model, 'Accord')
        self.assertEqual(self.vehicle.weight, 1500)
        self.assertEqual(self.vehicle.booking, self.booking)

    def test_vehicle_str(self):
        self.assertEqual(str(self.vehicle), '1HGCM82633A123456')
