from django.urls import path
from . import views

urlpatterns = [
    path('file/',views.update_excel.as_view(), name='file_data_to_db')
]
