from django.shortcuts import render
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

geocodingapi = "https://geocoding-api.open-meteo.com/v1/search?name={}&count=1"
weatherapi = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
WMO_WEATHER_CODES = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "🌤️"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        61: ("Rain: Slight", "🌦️"),
        95: ("Thunderstorm: Slight", "⛈️"),
        # Add other codes if needed
    }


class get_weather(APIView):
    def get(self,request):

        context= {}
        try:
            city = request.query_params.get('city')
            if not city:
                city = "tenkasi" 
        except:
            city = "tenkasi"
        
        location_url = geocodingapi.format(city)

        try:
            location = requests.get(location_url,timeout=10).json()
            latitude = location['results'][0]['latitude']
            longitude = location['results'][0]['longitude']
            name = location['results'][0]['name']
            population = location['results'][0]['population']
            context['name'] = name

        except Exception as e:
            context['message'] = "no city found"
            print({"error":str(e)})

            return render(request,'weather.html',context)

        weather_url = weatherapi.format(latitude=latitude,longitude=longitude)
        weather_data = requests.get(weather_url).json()

        weather = weather_data.get('current_weather')
        units = weather_data.get('current_weather_units')

        description, symbol = WMO_WEATHER_CODES.get(weather['weathercode'],("Unknown", "❓"))

        current_weather = {
            "time":f"{weather['time']}",
            "temperature":f"{weather['temperature']} {units['temperature']}",
            "windspeed":f"{weather['windspeed']} {units['windspeed']}",
            "description":description,            
            "symbol":symbol,
            "is_day":weather['is_day'],
            "population":population,
            # "interval":f"{weather['interval']} {units['interval']}",
            # "winddirection":f"{weather['winddirection']} {units['winddirection']}",
            }

        context['current_weather'] = current_weather

        # print(">>>>>",request.headers.get('Accept'))
        return render(request,'weather.html',context)
        return Response({"status":"success","data":context},status=status.HTTP_200_OK)   

class weather_graph(APIView):

    def post(self,request):
        data = request.POST
        
