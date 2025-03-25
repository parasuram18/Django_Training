from django.urls import path
from . import views
urlpatterns = [
    path('task/',views.task,name='task'),
    path('mail/',views.mail,name='send_mail'),
    path('alltasks/',views.get_all_tasks,name='alltasks'),
    path('deactivate/',views.deactive_tasks,name='deactivate'),
    path('every_10/',views.intervel_task,name='Intervel_task'),
    path('every_day/',views.crontab_task,name='crontab_task'),
]
