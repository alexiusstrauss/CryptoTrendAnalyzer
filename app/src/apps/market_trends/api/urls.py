from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CurrencyDataViewSet

router = DefaultRouter()
router.register(r'(?P<pair>BRLBTC|BRLETH)/mms', CurrencyDataViewSet, basename='currencydata')

urlpatterns = [
    path('', include(router.urls)),
]
