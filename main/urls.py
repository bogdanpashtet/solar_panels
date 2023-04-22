from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('calc/', calculate, name='calc'),
    path('station/<int:id>/', StationInfo.as_view()),
]
