from fpdf import FPDF
from datetime import datetime
import os

def create_pdf_report(current_data, forecast_data, unit='metric', lang='en', filename="weather_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    city_name = current_data.get('name', 'Unknown City')
    country = current_data.get('sys', {}).get('country', '')
    pdf.cell(200, 10, txt=f"Weather Report: {city_name}, {country}", ln=True, align='C')
    pdf.ln(10)
    
    # Current Weather
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Current Weather", ln=True)
    pdf.set_font("Arial", '', 11)
    
    temp_unit = "C" if unit == "metric" else "F"
    temp = current_data['main']['temp']
    desc = current_data['weather'][0]['description'].capitalize()
    humidity = current_data['main']['humidity']
    wind_speed = current_data['wind']['speed']
    
    pdf.cell(200, 8, txt=f"Temperature: {temp} {temp_unit}", ln=True)
    pdf.cell(200, 8, txt=f"Condition: {desc}", ln=True)
    pdf.cell(200, 8, txt=f"Humidity: {humidity}%", ln=True)
    pdf.cell(200, 8, txt=f"Wind Speed: {wind_speed} {'m/s' if unit == 'metric' else 'mph'}", ln=True)
    pdf.ln(10)
    
    # Forecast
    if forecast_data:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="5-Day Forecast (3-Hour Intervals)", ln=True)
        pdf.set_font("Arial", '', 10)
        
        # Table Header
        pdf.cell(50, 8, "Date/Time", border=1)
        pdf.cell(40, 8, "Temp", border=1)
        pdf.cell(60, 8, "Condition", border=1)
        pdf.cell(40, 8, "Wind", border=1)
        pdf.ln()
        
        for item in forecast_data['list']:
            dt_txt = item['dt_txt']
            ftemp = item['main']['temp']
            fdesc = item['weather'][0]['description'].capitalize()
            fwind = item['wind']['speed']
            
            pdf.cell(50, 8, dt_txt, border=1)
            pdf.cell(40, 8, f"{ftemp} {temp_unit}", border=1)
            pdf.cell(60, 8, fdesc, border=1)
            pdf.cell(40, 8, str(fwind), border=1)
            pdf.ln()

    report_path = os.path.join(os.getcwd(), filename)
    pdf.output(report_path)
    return report_path
