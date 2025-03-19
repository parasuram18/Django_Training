from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import treatment_charges,lab_charges,consultant_charges,room_master,change_prices,finance,hosphital_details
from . import pricing
from django.db.models import F
import time, threading
# Create your views here.

class create_data(APIView):
    def post(self, request):
        raw_data = request.data
        
        for data in raw_data:
            change_prices.objects.create(rate_plan=data['rate_plan'], amount=data['amount'])
        
        return Response({'message':"data added succesfully"},status=status.HTTP_201_CREATED)
    
class update_billing(APIView):
    def put(self,request):
        start = time.time()
        data = request.data
        
        method = data['method']
        percentage = data['percentage']
        amount = data['amount']
        apply_by = data['apply_by']
        
        thread = threading.Thread(target=pricing.update_billing_models,args=(method, apply_by, amount, percentage),name='update')
        
        thread.start()
        # thread.join()
        
        end = time.time()
        
        return Response({'message':"charges modified succesfully",'time':end-start},status=status.HTTP_201_CREATED)

        