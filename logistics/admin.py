from django.contrib import admin
from .models import Booking, Vehicle

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date')
    search_fields = ('booking_number', 'loading_port', 'discharge_port')
    list_filter = ('loading_port', 'discharge_port', 'ship_arrival_date', 'ship_departure_date')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vin', 'make', 'model', 'weight', 'booking')
    search_fields = ('vin', 'make', 'model')
    list_filter = ('make', 'model', 'booking')
