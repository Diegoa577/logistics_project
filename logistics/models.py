from django.db import models

class Booking(models.Model):
    booking_number = models.CharField(max_length=50, unique=True)
    loading_port = models.CharField(max_length=100)
    discharge_port = models.CharField(max_length=100)
    ship_arrival_date = models.DateField()
    ship_departure_date = models.DateField()

    def __str__(self):
        return self.booking_number

class Vehicle(models.Model):
    vin = models.CharField(max_length=50, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.FloatField()
    booking = models.ForeignKey(Booking, related_name='vehicles', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.vin
