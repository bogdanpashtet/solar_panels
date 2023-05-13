import csv

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api.utils import *
import pandas as pd
from main.models import *


@require_http_methods(["GET"])
def station_info_get(request, **kwargs):
    data = Stations.objects.filter(id=kwargs['id']).values()
    return JsonResponse(list(data), safe=False)


@require_http_methods(["GET"])
def stations_info_get(request):
    data = list(Stations.objects.values())
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def station_albedo_get(request, **kwargs):
    data = list(Albedo.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


# diffuse solar radiation
@require_http_methods(["GET"])
def stations_diffuse_daily_get(request, **kwargs):
    data = list(DiffuseDailySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def stations_diffuse_monthly_get(request, **kwargs):
    data = list(DiffuseMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def stations_diffuse_hourly_get(request, **kwargs):
    station_id = (kwargs['id'] - 1) * 24 + 1
    data = list(DiffuseHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                           station_id_id__lte=station_id + 23).values())
    return JsonResponse(data, safe=False)


# total solar radiation
@require_http_methods(["GET"])
def stations_total_daily_get(request, **kwargs):
    data = list(TotalDailySolarRadiation.objects.filter(station_id=kwargs["id"]).values())
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def stations_total_monthly_get(request, **kwargs):
    data = list(TotalMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def stations_total_hourly_get(request, **kwargs):
    # это заглушка, потому что данные в базе лежат криво, а лазить и менять id в ~12000 строках я не хочу (датасеты формаировал, к сожалению, не я)
    # поэтому делаем выборку с 3985 индекса и по каджому часу. аналогично и в других "часовых" данных, только там индексация начинается с единицы
    # в целом добавление в базу новых данных не предполагается, так как база не менялась с 2004, так что пойдет и так
    station_id = (kwargs['id'] - 1) * 24 + 3985
    data = list(TotalHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                         station_id_id__lte=station_id + 23).values())
    return JsonResponse(data, safe=False)


# total solar radiation
@require_http_methods(["GET"])
def stations_direct_daily_get(request, **kwargs):
    data = list(DirectDailySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def stations_direct_monthly_get(request, **kwargs):
    data = list(DirectMonthlySolarRadiation.objects.filter(station_id=kwargs['id']).values())
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def stations_direct_hourly_get(request, **kwargs):
    station_id = (kwargs['id'] - 1) * 24 + 1
    data = list(DirectHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                          station_id_id__lte=station_id + 23).values())
    return JsonResponse(data, safe=False)


# API методы для скачивания CSV
@require_http_methods(["GET"])
def stations_diffuse_hourly_get_csv(request, **kwargs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + str(kwargs['id']) + '_diffuse_hourly' + '.csv"'

    station_id = (kwargs['id'] - 1) * 24 + 1
    data = DiffuseHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                      station_id_id__lte=station_id + 23).values()

    writer = csv.writer(response)
    write_data_hourly(writer, data)

    return response


@require_http_methods(["GET"])
def stations_total_hourly_get_csv(request, **kwargs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + str(kwargs['id']) + '_total_hourly' + '.csv"'

    station_id = (kwargs['id'] - 1) * 24 + 3985
    data = TotalHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                    station_id_id__lte=station_id + 23).values()

    writer = csv.writer(response)
    write_data_hourly(writer, data)

    return response


@require_http_methods(["GET"])
def stations_direct_hourly_get_csv(request, **kwargs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + str(kwargs['id']) + '_direct_hourly' + '.csv"'

    station_id = (kwargs['id'] - 1) * 24 + 1
    data = DirectHourlySolarRadiation.objects.filter(station_id_id__gte=station_id,
                                                     station_id_id__lte=station_id + 23).values()

    writer = csv.writer(response)
    write_data_hourly(writer, data)

    return response


@csrf_exempt
@require_http_methods(["POST"])
def calc_by_day(request):
    try:
        data = pd.read_csv(get_file(request), decimal=",", delimiter=';')
    except Exception as e:
        print("Ошибка при чтении csv файла: ", e)
        return HttpResponseBadRequest('Invalid data')

    res = CalculateByDay(data, request).get_dataset()
    res_json = pd.Series(res).to_json(orient='values')
    return JsonResponse(res_json, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def calc_by_month(request):
    try:
        data = pd.read_csv(get_file(request), decimal=",", delimiter=';')
    except Exception as e:
        print("Ошибка при чтении csv файла: ", e)
        return HttpResponseBadRequest('Invalid data')

    res = CalculateByMonth(data, request).get_dataset()
    res_json = pd.Series(res).to_json(orient='values')
    return JsonResponse(res_json, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def calc_by_year(request):
    try:
        data = pd.read_csv(get_file(request), decimal=",", delimiter=';')
    except Exception as e:
        print("Ошибка при чтении csv файла: ", e)
        return HttpResponseBadRequest('Invalid data')

    res = CalculateByYear(data, request).get_dataset()
    res_json = pd.Series(res).to_json(orient='values')
    return JsonResponse(res_json, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def calc_by_custom(request):
    try:
        data = pd.read_csv(get_file(request), decimal=",", delimiter=';')
    except Exception as e:
        print("Ошибка при чтении csv файла: ", e)
        return HttpResponseBadRequest('Invalid data')

    res = CalculateByCustom(data, request).get_dataset()
    res_json = pd.Series(res).to_json(orient='values')
    return JsonResponse(res_json, safe=False)
