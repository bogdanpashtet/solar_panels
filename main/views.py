from django.shortcuts import render
from django.views.generic import ListView
from insolation_for_horizontal_panels.models import *


def index(request):
    return render(request, 'index.html')


class StationInfo(ListView):
    model = Stations
    template_name = 'stations_info.html'


def calculate(request):
    return render(request, 'calculate.html')
