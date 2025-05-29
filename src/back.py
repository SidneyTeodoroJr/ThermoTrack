import time
import requests
from datetime import datetime

API_BASE_URL = "http://localhost:8000"  # adjust if your server is elsewhere

def query_temperature(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        temperature = float(data['current_condition'][0]['temp_C'])
        print(f"[{datetime.now()}] {city} temperature: {temperature}°C")
        return temperature
    except Exception as e:
        print(f"Error querying temperature: {e}")
        return None

def calculate_efficiency(temperature):
    if temperature >= 28:
        return 100.0
    elif temperature <= 24:
        return 75.0
    else:
        eff = 75 + ((temperature - 24) * (25 / 4))  # Linear interpolation
        return round(min(eff, 100.0), 2)

def insert_data_via_api(temperature, efficiency):
    try:
        # Assuming there is a POST /records route to insert data (if not, keep insert_data with SQLite)
        url = f"{API_BASE_URL}/records"
        payload = {
            "datetime": datetime.now().isoformat(sep=' ', timespec='seconds'),
            "temperature": temperature,
            "efficiency": efficiency
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Data inserted via API: {temperature}°C, Efficiency: {efficiency}%")
    except Exception as e:
        print(f"Error inserting data via API: {e}")

def update_data(city):
    while True:
        temperature = query_temperature(city)
        if temperature is not None:
            efficiency = calculate_efficiency(temperature)
            # If there is no POST on the API, you can call the old insert_data function
            insert_data_via_api(temperature, efficiency)
        time.sleep(30)

def get_last_datetime():
    try:
        url = f"{API_BASE_URL}/latest"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        record = response.json()
        datetime_str = record.get("datetime")
        if datetime_str:
            print(f"Last reading obtained via API: {datetime_str}")
            return datetime_str
        else:
            print("No date available in API")
            return None
    except Exception as e:
        print(f"Error fetching last datetime via API: {e}")
        return None
