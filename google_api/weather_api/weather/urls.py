from django.urls import path
from .views import get_weather

urlpatterns = [
    path('get/',get_weather.as_view(),name='get_weather')
]
