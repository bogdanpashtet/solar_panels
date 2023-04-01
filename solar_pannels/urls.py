from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name=''),
    path('station/<int:id>', StationInfo.as_view()),

    # API methods
    path('api/v1/stations', stations_info_get),
    path('api/v1/station/<int:id>', station_info_get),

    path('api/v1/station/<int:id>/diffuse-daily', stations_diffuse_daily_get),
    path('api/v1/station/<int:id>/diffuse-monthly', stations_diffuse_monthly_get),
    path('api/v1/station/<int:id>/diffuse-hourly', stations_diffuse_hourly_get),

    path('api/v1/station/<int:id>/total-daily', stations_total_daily_get),
    path('api/v1/station/<int:id>/total-monthly', stations_total_monthly_get),
    path('api/v1/station/<int:id>/total-hourly', stations_total_hourly_get),

    path('api/v1/station/<int:id>/direct-daily', stations_direct_daily_get),
    path('api/v1/station/<int:id>/direct-monthly', stations_direct_monthly_get),
    path('api/v1/station/<int:id>/direct-hourly', stations_direct_hourly_get),

]
