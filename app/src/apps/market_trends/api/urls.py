from django.urls import re_path

from .views import CurrencyDataViewSet

urlpatterns = [
    re_path(r'^(?P<pair>BRLBTC|BRLETH)/mms/$', CurrencyDataViewSet.as_view({'get': 'list'}), name='currencydata-mms-list'),
]
