from django.shortcuts import render
from .tasks import add,send_mail_to
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
# Create your views here.

@api_view(['POST'])
def task(request):
    try:
        start = time.time()
        result = add.delay(3,5)
        print(result.get())
        # result = add.apply_async(args=(3,5),task_id='add')
        end = time.time()
        
        # return Response({'message':'success',"Task id": result.id,"Task result": result.get(), 'time':end-start},status=status.HTTP_200_OK)
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