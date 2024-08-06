from django.core.management.base import BaseCommand
from logistics.models import Vehicle, Booking
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete vehicles with a booking ship arrival date older than 6 months'

    def handle(self, *args, **kwargs):
        six_months_ago = timezone.now().date() - timedelta(days=6*30)
        old_vehicles = Vehicle.objects.filter(booking__ship_arrival_date__lt=six_months_ago)
        count = old_vehicles.count()
        old_vehicles.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} old vehicles'))
