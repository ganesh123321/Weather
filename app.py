import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
import geocoder
import os
from weather_api import get_current_weather, get_forecast, get_weather_by_coords, get_forecast_by_coords
from pdf_generator import create_pdf_report

# Must be the first Streamlit command
st.set_page_config(page_title="Modern Weather App", page_icon="🌤️", layout="wide")

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Animated Dynamic Background */
    .stApp {
        background: linear-gradient(-45deg, #0b1120, #1e3a5f, #3362a2, #0b1120);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Layout adjustments */
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }

    /* Glassmorphism for Metric Cards & General Containers */
    [data-testid="stMetric"], .metric-card {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }

    /* Interactive Hover Gestures for Cards */
    [data-testid="stMetric"]:hover, .metric-card:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 15px 40px 0 rgba(0, 0, 0, 0.4) !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
    }

    /* Sidebar Frost Effect */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Interactive Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
        filter: brightness(1.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None
if "forecast_data" not in st.session_state:
    st.session_state.forecast_data = None
if "current_search" not in st.session_state:
    st.session_state.current_search = {"type": None, "query": None, "unit": None, "lang": None}

def add_to_recent(city):
    if city and city not in st.session_state.recent_searches:
        st.session_state.recent_searches.insert(0, city)
        if len(st.session_state.recent_searches) > 5:
            st.session_state.recent_searches.pop()

def fetch_weather(city=None, lat=None, lon=None, unit='metric', lang='en'):
    with st.spinner("Fetching weather data..."):
        if city:
            current = get_current_weather(city, lang=lang, unit=unit)
            forecast = get_forecast(city, lang=lang, unit=unit)
            search_type = 'city'
            query = city
        elif lat and lon:
            current = get_weather_by_coords(lat, lon, lang=lang, unit=unit)
            forecast = get_forecast_by_coords(lat, lon, lang=lang, unit=unit)
            search_type = 'coords'
            query = (lat, lon)
        else:
            return

        if current and current.get("cod") == 200:
            st.session_state.weather_data = current
            st.session_state.forecast_data = forecast
            st.session_state.current_search = {"type": search_type, "query": query, "unit": unit, "lang": lang}
            if city:
                add_to_recent(city)
            st.toast(f"Successfully loaded weather for {current.get('name')}!", icon="✨")
        else:
            st.error("Error fetching data. Please check the city name or API Key.")

# --- SIDEBAR ---
st.sidebar.title("⚙️ Settings & Search")

# Language and Unit selection
col1, col2 = st.sidebar.columns(2)
unit_selection = col1.selectbox("Unit", ["Celsius", "Fahrenheit"])
unit_param = "metric" if unit_selection == "Celsius" else "imperial"

lang_selection = col2.selectbox("Language", ["English (en)", "Spanish (es)", "French (fr)", "German (de)", "Hindi (hi)"])
lang_param = lang_selection.split("(")[1].replace(")", "")

# Auto-refresh if language or unit changed
if st.session_state.current_search["type"]:
    last_search = st.session_state.current_search
    if last_search["unit"] != unit_param or last_search["lang"] != lang_param:
        if last_search["type"] == 'city':
            fetch_weather(city=last_search["query"], unit=unit_param, lang=lang_param)
        elif last_search["type"] == 'coords':
            lat, lon = last_search["query"]
            fetch_weather(lat=lat, lon=lon, unit=unit_param, lang=lang_param)

# Search Input
city_input = st.sidebar.text_input("Enter City Name:", placeholder="e.g. London, New York")
if st.sidebar.button("Search City", use_container_width=True):
    if city_input:
        fetch_weather(city=city_input, unit=unit_param, lang=lang_param)
    else:
        st.sidebar.warning("Please enter a city name.")

# Auto-detect location
st.sidebar.markdown("---")
if st.sidebar.button("📍 Use My Location", use_container_width=True):
    g = geocoder.ip('me')
    if g.latlng:
        fetch_weather(lat=g.latlng[0], lon=g.latlng[1], unit=unit_param, lang=lang_param)
    else:
        st.sidebar.error("Could not detect location.")

# Recent Searches
if st.session_state.recent_searches:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Recent Searches")
    for recent_city in st.session_state.recent_searches:
        if st.sidebar.button(f"🔍 {recent_city}", key=f"recent_{recent_city}", use_container_width=True):
            fetch_weather(city=recent_city, unit=unit_param, lang=lang_param)

# --- MAIN DASHBOARD ---
st.title("🌤️ Weather Forecast Application")

if not os.getenv("OPENWEATHER_API_KEY") or os.getenv("OPENWEATHER_API_KEY") == "your_api_key_here":
    st.warning("⚠️ OpenWeather API Key is not configured. Please add your key to the `.env` file to see real weather data.")

if st.session_state.weather_data:
    current = st.session_state.weather_data
    forecast = st.session_state.forecast_data
    
    city_name = current.get('name', 'Unknown')
    country = current.get('sys', {}).get('country', '')
    desc = current['weather'][0]['description'].title()
    temp = current['main']['temp']
    icon_code = current['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
    
    temp_symbol = "°C" if unit_param == "metric" else "°F"
    wind_symbol = "m/s" if unit_param == "metric" else "mph"

    # Top Section: Current Weather Overview
    st.markdown("---")
    colA, colB = st.columns([1, 2])
    with colA:
        st.image(icon_url, width=150)
    with colB:
        st.markdown(f"## {city_name}, {country}")
        st.markdown(f"**Condition:** {desc}")
        st.markdown(f"## {temp} {temp_symbol}")

    # Metrics Section
    st.markdown("### Current Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("💧 Humidity", f"{current['main']['humidity']} %")
    m2.metric("🌬️ Wind Speed", f"{current['wind']['speed']} {wind_symbol}")
    m3.metric("⏱️ Pressure", f"{current['main']['pressure']} hPa")
    m4.metric("👁️ Visibility", f"{current.get('visibility', 0) / 1000} km")

    # Sunrise / Sunset (adjusted for city time zone)
    tz_offset = current.get('timezone', 0)
    sunrise_dt = datetime.fromtimestamp(current['sys']['sunrise'], timezone.utc) + timedelta(seconds=tz_offset)
    sunset_dt = datetime.fromtimestamp(current['sys']['sunset'], timezone.utc) + timedelta(seconds=tz_offset)
    sunrise_time = sunrise_dt.strftime('%I:%M %p')
    sunset_time = sunset_dt.strftime('%I:%M %p')
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"🌅 **Sunrise:** {sunrise_time}")
    with c2:
        st.info(f"🌇 **Sunset:** {sunset_time}")

    # --- FORECAST TABS ---
    st.markdown("---")
    tab1, tab2 = st.tabs(["📊 Hourly Forecast Chart", "📅 5-Day Forecast"])

    if forecast and 'list' in forecast:
        timestamps = []
        temps = []
        
        tz_offset = current.get('timezone', 0)
        for item in forecast['list'][:10]: # Next 30 hours approx
            dt = datetime.fromtimestamp(item['dt'], timezone.utc) + timedelta(seconds=tz_offset)
            timestamps.append(dt.strftime('%d %b\n%H:%M'))
            temps.append(item['main']['temp'])

        with tab1:
            st.markdown("### Next 30 Hours Temperature Trend")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(timestamps, temps, marker='o', linestyle='-', color='#1f77b4', linewidth=2, markersize=8)
            ax.set_xlabel("Time", fontsize=10)
            ax.set_ylabel(f"Temperature ({temp_symbol})", fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # Highlight max temp feeling
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)
            for spine in ax.spines.values():
                spine.set_color('#aaaaaa')
            ax.tick_params(colors='#aaaaaa', which='both')
            ax.yaxis.label.set_color('#aaaaaa')
            ax.xaxis.label.set_color('#aaaaaa')
            ax.title.set_color('#aaaaaa')
            
            st.pyplot(fig)

        with tab2:
            st.markdown("### 5-Day Forecast (3-Hour Intervals)")
            
            # Simple list iteration to display forecast
            forecast_cols = st.columns(5)
            # Group by day could be complex, we just show a scrollable or subset of cards
            # Showing 1 item per day approximation (every 8th item)
            daily_forecast = forecast['list'][::8][:5]
            
            for idx, item in enumerate(daily_forecast):
                col = forecast_cols[idx % 5]
                with col:
                    dt = datetime.fromtimestamp(item['dt'], timezone.utc) + timedelta(seconds=tz_offset)
                    f_temp = item['main']['temp']
                    f_desc = item['weather'][0]['description'].title()
                    f_icon = item['weather'][0]['icon']
                    st.markdown(f"**{dt.strftime('%a, %d %b')}**")
                    st.image(f"http://openweathermap.org/img/wn/{f_icon}@2x.png", width=50)
                    st.markdown(f"**{f_temp} {temp_symbol}**")
                    st.caption(f_desc)

    # --- PDF EXPORT ---
    st.markdown("---")
    st.markdown("### Export Report")
    if st.button("📄 Generate PDF Report"):
        filename = f"weather_report_{city_name.replace(' ', '_')}.pdf"
        report_path = create_pdf_report(current, forecast, unit=unit_param, lang=lang_param, filename=filename)
        with open(report_path, "rb") as pdf_file:
            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_file,
                file_name=filename,
                mime="application/pdf"
            )
else:
    st.info("👈 Please search for a city or use your location in the sidebar to view weather data.")
