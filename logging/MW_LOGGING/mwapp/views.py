from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import sample
# Create your views here.
import sys, traceback

def a1():
    print(ad)

@api_view(['POST'])
def sample_func(request):

    data = request.data.get('data')
    name = data.get('name')
    print(ad)
    sample.objects.create(name=name)
    try:
        sample.objects.create(name=name)
    except Exception as e:
        # traceback.print_exc()
        tb = traceback.extract_tb(e.__traceback__)
        print(tb[0])
        print(tb[0].line)
        print(tb[0].lineno)
    if not data:
        return Response({'message':'no data recieved'},status=status.HTTP_400_BAD_REQUEST)
    # print(1/0)
    return Response({'message':'sample test success'},status=status.HTTP_200_OK)

@api_view(['GET'])
def success(request):

    data = request.data.get('data')
    print(data)

    # if not data:
    #     return Response({'message':'no data recieved'},status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'sample test success'},status=status.HTTP_200_OK)
