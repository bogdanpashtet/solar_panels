from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from calculations.utils import *
import pandas as pd


@csrf_exempt
@require_http_methods(["POST"])
def calc_by_day_csv(request):
    try:
        data = pd.read_csv(get_file(request), decimal=",", delimiter=';')
    except Exception as e:
        print("Ошибка при чтении csv файла: ", e)
        return HttpResponseBadRequest('Invalid data')

    return CalculateByDay(data, request).get_dataset()


@csrf_exempt
@require_http_methods(["POST"])
def calc_by_month_csv(request):
    try:
        data = pd.read_csv(get_file(request), decimal=",", delimiter=';')
    except Exception as e:
        print("Ошибка при чтении csv файла: ", e)
        return HttpResponseBadRequest('Invalid data')

    return CalculateByMonth(data, request).get_dataset()


@csrf_exempt
@require_http_methods(["POST"])
def calc_by_year_csv(request):
    try:
        data = pd.read_csv(get_file(request), decimal=",", delimiter=';')
    except Exception as e:
        print("Ошибка при чтении csv файла: ", e)
        return HttpResponseBadRequest('Invalid data')

    return CalculateByYear(data, request).get_dataset()


@csrf_exempt
@require_http_methods(["POST"])
def calc_by_custom_csv(request):
    try:
        data = pd.read_csv(get_file(request), decimal=",", delimiter=';')
    except Exception as e:
        print("Ошибка при чтении csv файла: ", e)
        return HttpResponseBadRequest('Invalid data')

    return CalculateByCustom(data, request).get_dataset()
