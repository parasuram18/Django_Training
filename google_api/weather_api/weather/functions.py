import requests




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


def get_current_weather(city):
        
    location_url = geocodingapi.format(city)
    try:
        location = requests.get(location_url,timeout=10).json()
        latitude = location['results'][0]['latitude']
        longitude = location['results'][0]['longitude']
        name = location['results'][0]['name']
        population = location['results'][0]['population']
    except Exception as e:
        print(f"ERROR : {str(e)}")
        return {}

    weather_url = weatherapi.format(latitude=latitude,longitude=longitude)
    weather_data = requests.get(weather_url).json()

    weather = weather_data.get('current_weather')
    units = weather_data.get('current_weather_units')

    description, symbol = WMO_WEATHER_CODES.get(weather['weathercode'],("Unknown", "❓"))

    current_weather = {
        "name":name,
        "time":f"{weather['time']}",
        "temperature":f"{weather['temperature']}",  # {units['temperature']}
        "windspeed":f"{weather['windspeed']} ",  #{units['windspeed']}
        "description":description,            
        "symbol":symbol,
        "is_day":weather['is_day'],
        "population":population,
        # "interval":f"{weather['interval']} {units['interval']}",
        # "winddirection":f"{weather['winddirection']} {units['winddirection']}",
        }
    return current_weather

def get_temperature(city):
    try:
        current_weater = get_current_weather(city)
        temperature = current_weater.get('temperature',0)
        return temperature# if temperature is not None else 0
    except Exception as e:
        print("Error---",str(e))    
        
def get_city_weather(city):
    current_weater = get_current_weather(city)
    name = current_weater.get('name')
    temperature = current_weater.get('temperature')
    
    return (name,float(temperature)) if name is not None else (city,0)
    