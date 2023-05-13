from django.urls import path
from api.views import *

urlpatterns = [
    path('stations', stations_info_get),
    path('station/<int:id>/', station_info_get),

    path('station/<int:id>/albedo', station_albedo_get),

    path('station/<int:id>/diffuse-daily', stations_diffuse_daily_get),
    path('station/<int:id>/diffuse-monthly', stations_diffuse_monthly_get),
    path('station/<int:id>/diffuse-hourly', stations_diffuse_hourly_get),

    path('station/<int:id>/total-daily', stations_total_daily_get),
    path('station/<int:id>/total-monthly', stations_total_monthly_get),
    path('station/<int:id>/total-hourly', stations_total_hourly_get),

    path('station/<int:id>/direct-daily', stations_direct_daily_get),
    path('station/<int:id>/direct-monthly', stations_direct_monthly_get),
    path('station/<int:id>/direct-hourly', stations_direct_hourly_get),

    # скачивание CSV
    path('station/<int:id>/diffuse-hourly/csv', stations_diffuse_hourly_get_csv),
    path('station/<int:id>/total-hourly/csv', stations_total_hourly_get_csv),
    path('station/<int:id>/direct-hourly/csv', stations_direct_hourly_get_csv),

    # расчет
    path('calc/by-day', calc_by_day),
    path('calc/by-month', calc_by_month),
    path('calc/by-year', calc_by_year),
    path('calc/by-custom', calc_by_custom),
]
