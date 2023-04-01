from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from main.models import *


def index(request):
    return render(request, 'index.html')


class StationInfo(ListView):
    model = Stations
    template_name = 'stations_info.html'
    extra_context = {'title': '?????????'}

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['station'] = Stations.objects.get(id=self.kwargs['id'])
        # context['albedo'] = model_to_dict(Albedo.objects.filter(station_id=self.kwargs['id']).first())
        #
        # context['diffuse_daily'] = DiffuseDailySolarRadiation.objects.get(station_id=self.kwargs['id'])
        # context['total_daily'] = TotalDailySolarRadiation.objects.get(station_id=self.kwargs['id'])
        # context['direct_daily'] = DirectDailySolarRadiation.objects.get(station_id=self.kwargs['id'])
        #
        # context['diffuse_monthly'] = DiffuseMonthlySolarRadiation.objects.get(station_id=self.kwargs['id'])
        # context['total_monthly'] = TotalMonthlySolarRadiation.objects.get(station_id=self.kwargs['id'])
        # context['direct_monthly'] = DirectMonthlySolarRadiation.objects.get(station_id=self.kwargs['id'])

        # context['diffuse_hourly'] = DiffuseHourlySolarRadiation.objects.get(station_id=self.kwargs['id'])
        # context['total_hourly'] = TotalHourlySolarRadiation.objects.get(station_id=self.kwargs['id'])
        # context['direct_hourly'] = DirectHourlySolarRadiation.objects.get(station_id=self.kwargs['id'])

        # return context


def station_info_get(request, **kwargs):
    data = Stations.objects.filter(id=kwargs['id']).values()
    return JsonResponse(list(data), safe=False)


def stations_info_get(request):
    data = list(Stations.objects.values())
    return JsonResponse(data, safe=False)


# diffuse solar radiation
def stations_diffuse_daily_get(request, **kwargs):
    data = list(DiffuseDailySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_diffuse_monthly_get(request, **kwargs):
    data = list(DiffuseMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_diffuse_hourly_get(request, **kwargs):
    data = list(DiffuseHourlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


# total solar radiation
def stations_total_daily_get(request, **kwargs):
    data = list(TotalDailySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_total_monthly_get(request, **kwargs):
    data = list(TotalMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_total_hourly_get(request, **kwargs):
    data = list(TotalHourlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


# total solar radiation
def stations_direct_daily_get(request, **kwargs):
    data = list(DirectDailySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_direct_monthly_get(request, **kwargs):
    data = list(DirectMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_direct_hourly_get(request, **kwargs):
    data = list(DirectHourlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)
