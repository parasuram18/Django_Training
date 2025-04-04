from django.urls import path
from . import views

urlpatterns = [
    path('logs/',views.sample_func, name="sample"),
    path('success/',views.success, name="success"),
]


