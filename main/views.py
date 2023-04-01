from django.shortcuts import render
from django.views.generic import ListView
from main.models import *


def index(request):
    return render(request, 'index.html')


class StationInfo(ListView):
    model = Stations
    template_name = 'stations_info.html'
    extra_context = {'title': '?????????'}
