# Modern Weather Forecast Application

A professional and modern weather application built with Python and Streamlit. It integrates with the OpenWeather API to provide real-time weather information and 5-day forecasts.

## Features
- **City Search**: Search weather for any city worldwide.
- **Auto-Detect Location**: Uses your IP to fetch local weather automatically.
- **Current Metrics**: Displays Temperature, Humidity, Wind Speed, Pressure, and Visibility.
- **5-Day Forecast**: Visually pleasing forecast cards.
- **Hourly Chart**: Visualizes the upcoming temperature trends using Matplotlib.
- **PDF Export**: Generate and download weather reports in PDF format.
- **Multi-language Support**: Supports English, Spanish, French, German, and Hindi.
- **Toggle Units**: Switch easily between Celsius and Fahrenheit.
- **Recent Searches**: Saves a history of your recent searches in the session.
- **Dark/Light Mode**: Natively supported by Streamlit (Settings -> Theme).

## Prerequisites
- Python 3.8+
- An OpenWeather API Key (Free tier)

## Installation

1. Switch to the project directory:
   ```bash
   cd weather_app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API Key:
   Open the `.env` file and replace `your_api_key_here` with your actual OpenWeather API key. You can get one for free at [openweathermap.org](https://openweathermap.org/).

4. Run the Application:
   ```bash
   streamlit run app.py
   ```

## Folder Structure
- `app.py`: Main Streamlit application frontend and layout.
- `weather_api.py`: Logic for communicating with the OpenWeather API.
- `pdf_generator.py`: Module for exporting data to PDF using FPDF.
- `.env`: Environment variables (API Keys).
- `requirements.txt`: Python package dependencies.
