from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


# def station(request):
#     return render(request, 'index.html')