from django.urls import path, include
from main.views import *

urlpatterns = [
    path('', include('main.urls')),
    path('api/v1/', include('api.urls')),
]
