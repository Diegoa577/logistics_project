import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from logistics.models import Booking, Vehicle
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit

def export_bookings_to_xls():
    bookings = Booking.objects.all().values()
    df = pd.DataFrame(bookings)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Bookings')
    writer.close() 
    output.seek(0)
    
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=bookings.xlsx'
    return response

def export_vehicles_to_xls():
    bookings = Vehicle.objects.all().values()
    df = pd.DataFrame(bookings)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Vehicles')
    writer.close() 
    output.seek(0)
    
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=vehicles.xlsx'
    return response

def export_bookings_to_pdf():
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=bookings.pdf'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    bookings = Booking.objects.all()
    width, height = letter
    margin = 40
    max_width = width - 2 * margin
    y = height - margin

    for booking in bookings:
        booking_info = f"- Booking Number: {booking.booking_number}, Loading Port: {booking.loading_port}, Discharge Port: {booking.discharge_port}, Ship arrival date: {booking.ship_arrival_date}, Ship departure date: {booking.ship_departure_date}"
        
        lines = simpleSplit(booking_info, 'Helvetica', 12, max_width)
        
        for line in lines:
            if y < margin:
                p.showPage()
                y = height - margin
            p.drawString(margin, y, line)
            y -= 20
        
        y -= 10
    
    p.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response


def export_vehicles_to_pdf():
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=vehicles.pdf'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    vehicles = Vehicle.objects.all()
    width, height = letter
    margin = 40
    max_width = width - 2 * margin
    y = height - margin

    for vehicle in vehicles:
        vehicle_info = f"- VIN Number: {vehicle.vin}, Make: {vehicle.make}, Model: {vehicle.model}, Weight: {vehicle.weight}"
        
        lines = simpleSplit(vehicle_info, 'Helvetica', 12, max_width)
        
        for line in lines:
            if y < margin:
                p.showPage()
                y = height - margin
            p.drawString(margin, y, line)
            y -= 20
        
        y -= 10
    
    p.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response
