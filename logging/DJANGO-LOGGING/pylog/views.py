import logging.config
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import logging
import traceback
# Create your views here.

logger = logging.getLogger('mylogger')
 
@api_view(['POST'])
def sample(request):
    try:
        data = request.data.get('data')
        if not data:
            return Response({'message':'no data recieved'},status=status.HTTP_200_OK)
        # print(1/0)
        return Response({'message':'sample test success', "error":1/0},status=status.HTTP_200_OK)
    except Exception as e:
        traceback_info = traceback.extract_tb(e.__traceback__)
        tb = traceback_info[-1]
        error_line_number = tb.lineno
        func_name = tb.name
        logger.error(f"Error occured in {func_name} at line {error_line_number}")
        return Response({'message':'Error occured',"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)