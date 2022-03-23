from django.urls import path

from .views import CalplanIndex, Holidays

urlpatterns = [
    path('', CalplanIndex.as_view(), name='home'),
    path('holidays/<int:year>/<str:region>', Holidays.as_view(), name='holidays'),
]