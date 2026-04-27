import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
print(f"API Key found: {API_KEY is not None}")

city = "London"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
r = requests.get(url)
data = r.json()

if r.status_code == 200:
    print(f"City Returned: {data.get('name')}, {data.get('sys', {}).get('country')}")
    print(f"Temperature: {data['main']['temp']} °C")
    print(f"Condition: {data['weather'][0]['description']}")
    print(f"Humidity: {data['main']['humidity']} %")
else:
    print("API Error:", data)
