import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

lat, lon = 13.0878, 80.2785
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
r = requests.get(url)
data = r.json()
print("Chennai from OpenWeather:")
print(f"Temperature: {data['main']['temp']} °C")
print(f"Condition: {data['weather'][0]['description']}")
print(f"Humidity: {data['main']['humidity']} %")
