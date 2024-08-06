import pandas as pd
from logistics.models import Booking, Vehicle

def import_bookings_from_xls(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        booking = Booking.objects.create(
            booking_number=row['booking_number'],
            loading_port=row['loading_port'],
            discharge_port=row['discharge_port'],
            ship_arrival_date=row['ship_arrival_date'],
            ship_departure_date=row['ship_departure_date'],
        )
        booking.save()

def import_vehicles_from_xls(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        vehicle = Vehicle.objects.create(
            vin=row['vin'],
            make=row['make'],
            model=row['model'],
            weight=row['weight'],
        )
        vehicle.save()
