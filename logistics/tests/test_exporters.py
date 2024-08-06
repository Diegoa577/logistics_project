"""
Test for exporters.
"""
from django.test import TestCase
from logistics.models import Booking, Vehicle
from logistics.utils.exporters import export_bookings_to_xls, export_bookings_to_pdf, export_vehicles_to_xls, export_vehicles_to_pdf
from datetime import date

class ExportersTest(TestCase):

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

    def test_export_bookings_to_xls(self):
        response = export_bookings_to_xls()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename=bookings.xlsx', response['Content-Disposition'])

    def test_export_bookings_to_pdf(self):
        response = export_bookings_to_pdf()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename=bookings.pdf', response['Content-Disposition'])

    def test_export_vehicles_to_xls(self):
        response = export_vehicles_to_xls()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename=vehicles.xlsx', response['Content-Disposition'])

    def test_export_vehicles_to_pdf(self):
        response = export_vehicles_to_pdf()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename=vehicles.pdf', response['Content-Disposition'])
