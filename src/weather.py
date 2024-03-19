import requests
import local_time
from config import settings

reference_hour = ""
actual_weather = ""

def weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?id={settings.weather_city}&appid={settings.weather_api_key}&units=metric&lang={settings.weather_language}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return f"Clima em {settings.city_name}: {weather_description}, Temperatura: {temperature}°C, Umidade: {humidity}%"
    else:
        return f"Não foi possível obter os dados do clima."
    
def weather_verify():
    global reference_hour
    global actual_weather
    if local_time.current_hour() != reference_hour:
        actual_weather = weather()
        reference_hour = local_time.current_hour()
    return actual_weather
