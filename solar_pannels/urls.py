from django.urls import path, include
from main.views import *

urlpatterns = [
    path('', include('main.urls')),
    path('insolation_for_horizontal_panels/v1/', include('insolation_for_horizontal_panels.urls')),
    path('insolation_for_horizontal_panels/v1/', include('calculations.urls')),
]
