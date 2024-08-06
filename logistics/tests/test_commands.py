"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase, TestCase
from logistics.models import Booking, Vehicle
from datetime import date, timedelta


@patch('django.db.utils.ConnectionHandler.__getitem__')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_getitem):
        """Test waiting for database if database ready."""
        patched_getitem.return_value = True

        call_command('wait_for_db')

        self.assertEqual(patched_getitem.call_count, 1)

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_getitem):
        """Test waiting for database when getting OperationalError."""
        patched_getitem.side_effect = [Psycopg2OpError] + \
            [OperationalError] * 5 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_getitem.call_count, 7)

class DeleteOldVehiclesCommandTest(TestCase):

    def setUp(self):
        self.old_booking = Booking.objects.create(
            booking_number='B12345',
            loading_port='Port A',
            discharge_port='Port B',
            ship_arrival_date=date.today() - timedelta(days=6*30+1),
            ship_departure_date=date.today() - timedelta(days=6*30+1)
        )
        self.new_booking = Booking.objects.create(
            booking_number='B67890',
            loading_port='Port C',
            discharge_port='Port D',
            ship_arrival_date=date.today(),
            ship_departure_date=date.today()
        )
        self.old_vehicle = Vehicle.objects.create(
            vin='1HGCM82633A123456',
            make='Honda',
            model='Accord',
            weight=1500,
            booking=self.old_booking
        )
        self.new_vehicle = Vehicle.objects.create(
            vin='1HGCM82633A654321',
            make='Toyota',
            model='Camry',
            weight=1600,
            booking=self.new_booking
        )

    def test_delete_old_vehicles(self):
        self.assertEqual(Vehicle.objects.filter(booking=self.old_booking).count(), 1)

        call_command('delete_old_vehicles')

        self.assertEqual(Vehicle.objects.filter(booking=self.old_booking).count(), 0)
        
        self.assertEqual(Vehicle.objects.filter(booking=self.new_booking).count(), 1)