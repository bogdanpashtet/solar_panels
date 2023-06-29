from django.urls import path
from calculations.views import *

urlpatterns = [
    # расчет
    path('calc/by-day/csv', calc_by_day_csv),
    path('calc/by-month/csv', calc_by_month_csv),
    path('calc/by-year/csv', calc_by_year_csv),
    path('calc/by-custom/csv', calc_by_custom_csv),
]