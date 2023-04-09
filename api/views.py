import csv

from django.http import JsonResponse, HttpResponse
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
    data = list(DiffuseHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                           station_id_id__lte=station_id + 23).values())
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
    data = list(TotalHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                         station_id_id__lte=station_id + 23).values())
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
    data = list(DirectHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                          station_id_id__lte=station_id + 23).values())
    return JsonResponse(data, safe=False)


def writeDataHourly(writer, data):
    writer.writerow(['hour_num', 'month_1', 'month_2', 'month_3', 'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9', 'month_10', 'month_11', 'month_12'])

    for i in data:
        writer.writerow([i["hour_num"], i["month_1"], i["month_2"], i["month_3"], i["month_4"], i["month_5"], i["month_6"], i["month_7"], i["month_8"], i["month_9"], i["month_10"], i["month_11"], i["month_12"]])


# API методы для скачивания CSV
def stations_diffuse_hourly_get_csv(request, **kwargs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + str(kwargs['id']) + '_diffuse_hourly' + '.csv"'

    station_id = (kwargs['id'] - 1) * 24 + 1
    data = DiffuseHourlySolarRadiation.objects.filter(station_id_id__gte=station_id, station_id_id__lte=station_id + 23).values()

    writer = csv.writer(response)
    writeDataHourly(writer, data)

    return response


def stations_total_hourly_get_csv(request, **kwargs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + str(kwargs['id']) + '_total_hourly' + '.csv"'

    station_id = (kwargs['id'] - 1) * 24 + 3985
    data = TotalHourlySolarRadiation.objects.filter(station_id_id__gte=station_id, station_id_id__lte=station_id + 23).values()

    writer = csv.writer(response)
    writeDataHourly(writer, data)

    return response


def stations_direct_hourly_get_csv(request, **kwargs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + str(kwargs['id']) + '_direct_hourly' + '.csv"'

    station_id = (kwargs['id'] - 1) * 24 + 1
    data = DirectHourlySolarRadiation.objects.filter(station_id_id__gte=station_id, station_id_id__lte=station_id + 23).values()

    writer = csv.writer(response)
    writeDataHourly(writer, data)

    return response