from django.shortcuts import render
from .tasks import add,send_mail_to
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
import json
from django_celery_beat.models import PeriodicTask,IntervalSchedule,CrontabSchedule,SolarSchedule,ClockedSchedule
from django.utils.timezone import now, timedelta
# Create your views here.

@api_view(['POST'])
def task(request):
    try:
        start = time.time()
        result = add.delay(3,5)
        print(result.get())
        end = time.time()
        
        return Response({'message':'success',"Task id": result.id,'time':end-start},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status':'Error','message':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def mail(request):
    try:
        start = time.time()
        
        to_mail = request.data.get('to_mail')
        
        result = send_mail_to.apply_async(args=(to_mail,),task_id=f'send_mail to {to_mail}')
        end = time.time()
        
        return Response({'status':'success',"Task id": result.id,'message':'Mail sent succesfully','time':end-start},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status':'Error','message':str(e)},status=status.HTTP_400_BAD_REQUEST)
    
# get all periotic tasks from celery-beat models 
@api_view(['GET'])
def get_all_tasks(request):

    tasks = PeriodicTask.objects.all().exclude(name="celery.backend_cleanup")
    task_details = [
        {
        "task_id":task.id,
        "task_name":task.name,
        "is_active":task.enabled
        } 
        for task in tasks]
    
    return Response({'status':'success','tasks':task_details},status=status.HTTP_200_OK)
    
# deactivate tasks by task id --> change "enabled" to false
@api_view(['GET'])
def deactive_tasks(request):

    data = request.query_params.getlist('id')

    for id in data:
        PeriodicTask.objects.filter(id=id).update(enabled=False)

    return Response({'status':'success','message':'Tasks deactivated ','data':data},status=status.HTTP_200_OK)
   
# shedule new intervel task 
@api_view(['POST'])
def intervel_task(request):
    
    to_mail = request.data.get('to_mail')
    # create a new schedule time in IntervalSchedule model 
    interval, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)
    # asign a task with interval obj as a foreign key
    PeriodicTask.objects.get_or_create(name='send_mail_at_every_1_minute',
                                       task='celery_test.tasks.send_mail_to',
                                       args=json.dumps([to_mail]),
                                       interval=interval)
    return Response({'status':'success','message':'task started succesfully'},status=status.HTTP_200_OK)

# shedule new crontab task 
@api_view(['POST'])
def crontab_task(request):
    
    to_mail = request.data.get('to_mail')
    # create a new schedule time in ContrabSchedule model 
    crontab, created = CrontabSchedule.objects.get_or_create(hour="15",minute="30", timezone='Asia/Kolkata')
    # asign a task with crontab obj as a foreign key
    PeriodicTask.objects.get_or_create(name='send_mail_at_every_eve',
                                       task='celery_test.tasks.send_mail_to',
                                       args=json.dumps([to_mail]),
                                       crontab=crontab)

    return Response({'status':'success','message':'tasks started succesfully'},status=status.HTTP_200_OK)


# interval, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)
# crontab, created = CrontabSchedule.objects.get_or_create(hour="15",minute="30", timezone='Asia/Kolkata')
# clock, created = ClockedSchedule.objects.get_or_create(clocked_time=now()+timedelta(minutes=5))
# solar, created = SolarSchedule.objects.get_or_create(event='sunrise', latitude=11.1271, longitude=78.6569)