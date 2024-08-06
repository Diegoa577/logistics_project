from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Vehicle
from .serializers import BookingSerializer, VehicleSerializer
from .utils.exporters import export_bookings_to_xls, export_bookings_to_pdf
from .utils.importers import import_bookings_from_xls
from faker import Faker

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

fake = Faker()

@api_view(['POST'])
def populate_database(request):
    for _ in range(50):
        booking = Booking.objects.create(
            booking_number=fake.unique.bothify(text='??#####'),
            loading_port=fake.city(),
            discharge_port=fake.city(),
            ship_arrival_date=fake.date_this_year(),
            ship_departure_date=fake.date_this_year(),
        )
        for _ in range(5):
            Vehicle.objects.create(
                vin=fake.unique.bothify(text='??#####'),
                make=fake.company(),
                model=fake.word(),
                weight=fake.random_number(digits=4),
                booking=booking,
            )
    return Response({"message": "Database populated with 50 random bookings and 250 vehicles."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def export_xls(request):
    return export_bookings_to_xls()

@api_view(['GET'])
def export_pdf(request):
    return export_bookings_to_pdf()

@api_view(['POST'])
def import_xls(request):
    file = request.FILES['file']
    import_bookings_from_xls(file)
    return Response({"message": "Database populated from XLS file."}, status=status.HTTP_201_CREATED)
