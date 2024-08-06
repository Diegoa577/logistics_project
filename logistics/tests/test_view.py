"""
Tests for the API.
"""
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from logistics.models import Booking, Vehicle
from datetime import date
from django.urls import reverse
from io import BytesIO
import pandas as pd

class BookingViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.booking_data = {
            'booking_number': 'B12345',
            'loading_port': 'Port A',
            'discharge_port': 'Port B',
            'ship_arrival_date': date(2024, 8, 1),
            'ship_departure_date': date(2024, 8, 5)
        }
        self.booking = Booking.objects.create(**self.booking_data)

    def test_create_booking(self):
        url = reverse('booking-list')
        new_booking_data = {
            'booking_number': 'B67890',
            'loading_port': 'Port X',
            'discharge_port': 'Port Y',
            'ship_arrival_date': '2024-08-10', 
            'ship_departure_date': '2024-08-15' 
        }
        response = self.client.post(url, new_booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_get_booking(self):
        url = reverse('booking-detail', args=[self.booking.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['booking_number'], self.booking.booking_number)

    def test_update_booking(self):
        url = reverse('booking-detail', args=[self.booking.id])
        updated_data = self.booking_data.copy()
        updated_data['loading_port'] = 'Port X'
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.loading_port, 'Port X')

    def test_delete_booking(self):
        url = reverse('booking-detail', args=[self.booking.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)

class VehicleViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.booking = Booking.objects.create(
            booking_number='B12345',
            loading_port='Port A',
            discharge_port='Port B',
            ship_arrival_date=date(2024, 8, 1),
            ship_departure_date=date(2024, 8, 5)
        )
        self.vehicle_data = {
            'vin': '1HGCM82633A123456',
            'make': 'Honda',
            'model': 'Accord',
            'weight': 1500,
            'booking': self.booking
        }
        self.vehicle = Vehicle.objects.create(**self.vehicle_data)

    def test_create_vehicle(self):
        url = reverse('vehicle-list')
        new_vehicle_data = {
            'vin': '1HGCM82633A654321',
            'make': 'Toyota',
            'model': 'Camry',
            'weight': 1600,
            'booking': self.booking.id 
        }
        response = self.client.post(url, new_vehicle_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 2)

    def test_get_vehicle(self):
        url = reverse('vehicle-detail', args=[self.vehicle.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vin'], self.vehicle.vin)

    def test_update_vehicle(self):
        url = reverse('vehicle-detail', args=[self.vehicle.id])
        print("testttt")
        print(url)
        updated_data = self.vehicle_data.copy()
        updated_data['make'] = 'Toyota'
        updated_data['booking'] = self.booking.id 
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.make, 'Toyota')

    def test_delete_vehicle(self):
        url = reverse('vehicle-detail', args=[self.vehicle.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.count(), 0)

class ExportViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
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
        url = reverse('export-bookings-xls')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_export_bookings_to_pdf(self):
        url = reverse('export-bookings-pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_export_vehicles_to_xls(self):
        url = reverse('export-vehicles-xls')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_export_vehicles_to_pdf(self):
        url = reverse('export-vehicles-pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')