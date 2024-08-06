# Logistics App Solution

## Overview

This project is a logistics management system designed to handle bookings and the vehicles associated with those bookings. It includes full CRUD functionality for bookings and vehicles, as well as the ability to associate and disassociate vehicles from bookings.

## Models

- **Booking**: Represents a booking with details such as booking number, ports, and dates.
- **Vehicle**: Represents a vehicle with details such as VIN, make, model, weight, and associated booking.

## API

- **Endpoints**:
  - `/bookings/`: CRUD operations for bookings.
  - `/vehicles/`: CRUD operations for vehicles.
  - `/api/docs/`: Documentation of the endpoints.
  - `/admin/`: Django admin.
  - `/export-bookings-xls/`:Export Bookings to XLS
  - `/export-bookings-pdf/`: Export Bookings to PDF
  - `/import-bookings-xls/`: Import Bookings from XLS
  - `/export-vehicles-xls/`: Export Vehicles to XLS
  - `/export-vehicles-pdf/`: Export Vehicles to PDF
  - `/import-vehicles-xls/`: Import Vehicles from XLS
  
## Management Command

- **delete_old_vehicles**: Deletes vehicles with a booking ship arrival date older than 6 months.
- **wait_db**: Wait db to avoid race condition.

## Features

- CRUD operations for Bookings and Vehicles
- Export Bookings and Vehicles to XLS and PDF formats
- Import Bookings from XLS files
- Command to delete vehicles with booking ship arrival dates older than 6 months
- Django Admin interface for managing Bookings and Vehicles

## Installation

### Prerequisites

- Python 3.9+
- Docker and Docker Compose

### Clone the Repository

```bash
git clone <repository-url>
cd logistics_project
```

### Setup Docker

Ensure you have Docker and Docker Compose installed on your machine.

### Build and Run the Docker Containers

```bash
docker-compose up --build
```

### Create a Superuser

To access the Django Admin interface, you need to create a superuser:

```bash
docker-compose exec logistics_project python manage.py createsuperuser
```

Follow the prompts to set up the superuser.

## Usage

### Access the Application

The application should be accessible at `http://127.0.0.1:8000/`.

### Access the Admin Interface

The Django Admin interface should be accessible at `http://127.0.0.1:8000/admin/`.

### Populate the Database with Sample Data

You can populate the database with 50 random bookings and 250 vehicles:

```bash
curl -X POST http://127.0.0.1:8000/populate-database/
```

### Add vehicle

You can add a vehicle to the database:

```bash
curl -X POST http://127.0.0.1:8000/api/vehicles/ -H "Content-Type: application/json" -d '{
  "vin": "1HGCM82633A123456",
  "make": "Honda",
  "model": "Accord",
  "weight": 1500,
  "booking": 1
}'

```

### Get Vehicle

You can retrieve a vehicle by its ID:

```bash
curl -X GET http://127.0.0.1:8000/api/vehicles/1/ -H "Content-Type: application/json"

```

### Update Vehicle

You can update an existing vehicle by its ID:

```bash
curl -X PUT http://127.0.0.1:8000/api/vehicles/1/ -H "Content-Type: application/json" -d '{
  "vin": "1HGCM82633A123456",
  "make": "Toyota",
  "model": "Camry",
  "weight": 1600,
  "booking": 1
}'

```

### Delete Vehicle

You can delete a vehicle by its ID:

```bash
curl -X DELETE http://127.0.0.1:8000/api/vehicles/1/ -H "Content-Type: application/json"

```

### Add booking

You can add a booking to the database:

```bash
curl -X POST http://127.0.0.1:8000/api/bookings/ -H "Content-Type: application/json" -d '{
  "booking_number": "B67890",
  "loading_port": "Port X",
  "discharge_port": "Port Y",
  "ship_arrival_date": "2024-08-10",
  "ship_departure_date": "2024-08-15"
}'

```

### Get booking

You can retrieve a booking by its ID:

```bash
curl -X GET http://127.0.0.1:8000/api/bookings/1/ -H "Content-Type: application/json"

```

### Update Booking

You can update an existing booking by its ID:

```bash
curl -X PUT http://127.0.0.1:8000/api/bookings/1/ -H "Content-Type: application/json" -d '{
  "booking_number": "B67890",
  "loading_port": "Port Z",
  "discharge_port": "Port W",
  "ship_arrival_date": "2024-08-12",
  "ship_departure_date": "2024-08-17"
}'

```

### Delete Booking

You can delete a booking by its ID:

```bash
curl -X DELETE http://127.0.0.1:8000/api/bookings/1/ -H "Content-Type: application/json"

```

### Export Data

- Export Bookings to XLS: `http://127.0.0.1:8000/export-bookings-xls/`
- Export Bookings to PDF: `http://127.0.0.1:8000/export-bookings-pdf/`
- Export Vehicles to XLS: `http://127.0.0.1:8000/export-vehicles-xls/`
- Export Vehicles to PDF: `http://127.0.0.1:8000/export-vehicles-pdf/`

### Import Data

You can import bookings from an XLS file:

```bash
curl -F 'file=@path/to/your/bookings.xlsx' http://127.0.0.1:8000/api/import-bookings-xls/
```

### Run the Command to Delete Old Vehicles

You can run the command to delete vehicles with a booking ship arrival date older than 6 months:

```bash
docker-compose exec logistics_project python manage.py delete_old_vehicles
```

## Testing

To run the tests for the application, use the following command:

```bash
docker-compose exec logistics_project python manage.py test logistics.tests
```

## Technical Considerations

- The application uses Django REST Framework for API endpoints.
- The `Faker` library is used to generate random data for populating the database.
- The `xlsxwriter` library is used for generating XLS files.
- The `reportlab` library is used for generating PDF files.
- The application uses Docker for containerization, making it easy to set up and run.
- The application uses Swagger for the API documentation.
