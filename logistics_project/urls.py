"""
URL configuration for logistics_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from logistics.views import BookingViewSet, VehicleViewSet, populate_database, export_xls, export_pdf, import_xls

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('populate-database/', populate_database, name='populate-database'),
    path('export-bookings-xls/', export_xls, name='export-bookings-xls'),
    path('export-bookings-pdf/', export_pdf, name='export-bookings-pdf'),
    path('export-vehicles-xls/', export_xls, name='export-vehicles-xls'),
    path('export-vehicles-pdf/', export_pdf, name='export-vehicles-pdf'),
    path('import-bookings-xls/', import_xls, name='import-bookings-xls'),
    path('import-vehicle-xls/', import_xls, name='import-vehicle-xls'),
]
