from django.shortcuts import render
from django.http import FileResponse,HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from weather import functions
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import plotly.express as px
import io
# Create your views here.
import numpy as np


class pie_chart(APIView):
    def post(self,request):
        try:
            data = request.data
            city1 = data.get("city1")
            city2 = data.get("city2")
            cities = [city1,city2]
            weather_1 = functions.get_current_weather(city1)
            weather_2 = functions.get_current_weather(city2)
            
            values = [weather_1['temperature'],weather_2['temperature']]
            plt.pie(values,labels=cities,autopct='%1.1f%%',startangle=90,)
            
            output = io.BytesIO()
            plt.savefig(output,format='jpg')
            plt.close()
            output.seek(0)
            return FileResponse(output,as_attachment=True,filename="chart.png")
            
        except Exception as e:
            return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
            

class compare_cities(APIView):
    def post(self,request):
        try:
            data = request.data
            
            city1 = data.get('city1')
            city2 = data.get('city2')
            print(">>")
            
            weather_1 = functions.get_current_weather(city1)
            weather_2 = functions.get_current_weather(city2)
            
            data = [weather_1,weather_2]
            
            if not weather_1 or not weather_2:
                return Response({"status":"error","message":"city not found"},status=status.HTTP_404_NOT_FOUND)
            
            cities = [city1,city2]
            city_1= [float(weather_1.get('temperature')),float(weather_1.get('windspeed'))]
            city_2 = [float(weather_2.get('temperature')),float(weather_2.get('windspeed'))]
            
            x = [x  for x in range(len(cities))]
            x = np.arange(len(cities))  # X-axis locations for cities

            width = 0.2  # Bar width

            plt.bar(x - width/2, city_1, width, label=city1)
            plt.bar(x + width/2, city_2, width, label=city2)

            plt.xticks(x,['Temperature','Windspeed'])
            plt.xlabel('Fields')
            plt.ylabel('values')
            plt.title("Temperature and windspeed Comparison")
            plt.legend(loc="best")

            output = io.BytesIO()
            plt.savefig(output,format='jpg')
            plt.close()
            output.seek(0)
            return FileResponse(output,as_attachment=True,filename="comparision_chart.png")
            
            return Response({"status":"success","message":"data get succesfully",'data':data},status=status.HTTP_200_OK)
        except Exception as e:
                return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
class temp_graph(APIView):
    def get(self,request):
        try:
            cities_list = request.query_params.get('cities')
            cities = cities_list.split(',')
            
            x_axis = [x for x in range(len(cities))]
            
            temperatures = [functions.get_temperature(city) for city in cities]
            
            plt.bar(x=x_axis,height=temperatures,bottom=0,width=0.2)
            plt.xticks(x_axis,cities)
            plt.xlabel('Cities')
            plt.ylabel('Temperature')
            plt.title("Temperature Bar Graph")
                        
            output = io.BytesIO()
            plt.savefig(output,format='jpg')
            plt.close()
            output.seek(0)
            return FileResponse(output,as_attachment=True,filename="temp_bar.png")                        

        except Exception as e:
                return Response({"status":"error","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
