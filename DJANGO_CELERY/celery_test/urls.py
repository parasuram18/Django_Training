from django.urls import path
from . import views
urlpatterns = [
    path('task/',views.task,name='task'),
    path('mail/',views.mail,name='send_mail')
]
