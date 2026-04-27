import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Support both Streamlit secrets (cloud) and .env (local)
try:
    import streamlit as st
    API_KEY = st.secrets.get("OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY"))
except Exception:
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_current_weather(city, lang='en', unit='metric'):
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units={unit}&lang={lang}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_forecast(city, lang='en', unit='metric'):
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units={unit}&lang={lang}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_weather_by_coords(lat, lon, lang='en', unit='metric'):
    url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={unit}&lang={lang}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_forecast_by_coords(lat, lon, lang='en', unit='metric'):
    url = f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units={unit}&lang={lang}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
