from django.urls import path
from api.views import *

urlpatterns = [
    path('stations', stations_info_get),
    path('station/<int:id>/', station_info_get),

    path('station/<int:id>/albedo', stations_albedo_get),

    path('station/<int:id>/diffuse-daily', stations_diffuse_daily_get),
    path('station/<int:id>/diffuse-monthly', stations_diffuse_monthly_get),
    path('station/<int:id>/diffuse-hourly', stations_diffuse_hourly_get),

    path('station/<int:id>/total-daily', stations_total_daily_get),
    path('station/<int:id>/total-monthly', stations_total_monthly_get),
    path('station/<int:id>/total-hourly', stations_total_hourly_get),

    path('station/<int:id>/direct-daily', stations_direct_daily_get),
    path('station/<int:id>/direct-monthly', stations_direct_monthly_get),
    path('station/<int:id>/direct-hourly', stations_direct_hourly_get),
]
