from django.http import JsonResponse
from main.models import *


def station_info_get(request, **kwargs):
    data = Stations.objects.filter(id=kwargs['id']).values()
    return JsonResponse(list(data), safe=False)


def stations_info_get(request):
    data = list(Stations.objects.values())
    return JsonResponse(data, safe=False)


def stations_albedo_get(request, **kwargs):
    data = list(Albedo.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


# diffuse solar radiation
def stations_diffuse_daily_get(request, **kwargs):
    data = list(DiffuseDailySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_diffuse_monthly_get(request, **kwargs):
    data = list(DiffuseMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_diffuse_hourly_get(request, **kwargs):
    station_id = (kwargs['id'] - 1) * 24 + 1
    data = list(DiffuseHourlySolarRadiation.objects.filter(station_id_id__gte=station_id, station_id_id__lte=station_id + 23).values())
    return JsonResponse(data, safe=False)


# total solar radiation
def stations_total_daily_get(request, **kwargs):
    data = list(TotalDailySolarRadiation.objects.filter(station_id=kwargs["id"]).values())
    return JsonResponse(data, safe=False)


def stations_total_monthly_get(request, **kwargs):
    data = list(TotalMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_total_hourly_get(request, **kwargs):
    # это заглушка, потому что данные в базе лежат криво, а лазить и менять id в ~12000 строках я не хочу (датасеты формаировал, к сожалению, не я)
    # поэтому делаем выборку с 3985 индекса и по каджому часу. аналогично и в других "часовых" данных, только там индексация начинается с единицы
    # в целом добавление в базу новых данных не предполагается, так как база не менялась с 2004, так что пойдет и так
    station_id = (kwargs['id'] - 1) * 24 + 3985
    data = list(TotalHourlySolarRadiation.objects.filter(station_id_id__gte=station_id, station_id_id__lte=station_id + 23).values())
    return JsonResponse(data, safe=False)


# total solar radiation
def stations_direct_daily_get(request, **kwargs):
    data = list(DirectDailySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_direct_monthly_get(request, **kwargs):
    data = list(DirectMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


def stations_direct_hourly_get(request, **kwargs):
    station_id = (kwargs['id'] - 1) * 24 + 1
    data = list(DirectHourlySolarRadiation.objects.filter(station_id_id__gte=station_id, station_id_id__lte=station_id + 23).values())
    return JsonResponse(data, safe=False)
