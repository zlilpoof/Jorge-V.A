import requests
import config

def weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?id={config.weather_city}&appid={config.weather_api_key}&units=metric&lang={config.weather_language}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return f"Clima em {config.city_name}: {weather_description}, Temperatura: {temperature}°C, Umidade: {humidity}%"
    else:
        return f"Não foi possível obter os dados do clima."