from django.urls import path
from . import views

urlpatterns = [
    path('create/',views.create_data.as_view(), name='update'),
    path('update/',views.update_billing.as_view(), name='update'),
]
