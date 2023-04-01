from django.contrib import admin
from django.urls import path, include
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name=''),
    path('station/<int:id>/', StationInfo.as_view()),

    path('api/v1/', include('json_api.urls'))
]
