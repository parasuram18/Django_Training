from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import functions
# Create your views here.


class get_weather(APIView):
    def get(self,request):

        context= {}
        try:
            city = request.query_params.get('city')
            if not city:
                city = "tenkasi" 
        except:
            city = "tenkasi"
        
        current_weather = functions.get_current_weather(city)
        
        if not current_weather:
            context['message'] = "no city found"
            # return render(request,'weather.html',context)
            return Response({"status":"success","message":"No city found"},status=status.HTTP_200_OK)   
        
                
        context['current_weather'] = current_weather

        # print(">>>>>",request.headers.get('Accept'))
        # return render(request,'weather.html',context)
        return Response({"status":"success","data":context},status=status.HTTP_200_OK)   


