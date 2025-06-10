from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import requests
from datetime import datetime
import pytz  # for timezone-aware datetime

# === CONFIGURATION ===
GOOGLE_MAPS_API_KEY = "AIzaSyBL0LZOV7y7iDjcyjp9PdODFfSNMATGYhA"

# === Load model and encoder ===
model = joblib.load("cyclone_model.pkl")
label_encoder = joblib.load("cyclone_label_encoder.pkl")

app = FastAPI()

# === Request Body ===
class CycloneRequest(BaseModel):
    lat: float
    lon: float

# === Reverse Geocoding Function ===
def reverse_geocode(lat: float, lon: float) -> str:
    url = (
        f"https://maps.googleapis.com/maps/api/geocode/json?"
        f"latlng={lat},{lon}&key={GOOGLE_MAPS_API_KEY}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        return "Unknown"

    data = response.json()
    results = data.get("results", [])
    if not results:
        return "Unknown"

    # Look for district, fallback to city, then state
    for result in results:
        for component in result.get("address_components", []):
            types = component["types"]
            if "administrative_area_level_3" in types or \
               "administrative_area_level_2" in types or \
               "locality" in types or \
               "administrative_area_level_1" in types:
                return component["long_name"].upper()

    return "Unknown"

# === Main Prediction Endpoint ===
@app.post("/predict")
def predict_cyclone(data: CycloneRequest):
    lat, lon = data.lat, data.lon

    # Reverse geocode to get district/city name
    try:
        location_name = reverse_geocode(lat, lon)
    except Exception as e:
        location_name = "Unknown"

    # Get current UTC time and date
    current_time = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    month = datetime.utcnow().month

    # Fetch weather data
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        response = requests.get(url)
        weather = response.json().get("current_weather", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather API error: {str(e)}")

    if not weather:
        raise HTTPException(status_code=500, detail="Weather data missing")

    usa_wind = weather.get("windspeed", 0)
    usa_pres = 950  # Replace with real data source if needed
    storm_speed = weather.get("windgusts", 20)
    storm_dir = weather.get("winddirection", 0)

    input_data = pd.DataFrame([{
    "USA_WIND": usa_wind,
    "USA_PRES": usa_pres,
    "LAT": lat,
    "LON": lon,
    "STORM_SPEED": storm_speed,
    "STORM_DIR": storm_dir,
    "MONTH": month
}])

    try:
        pred_encoded = model.predict(input_data)[0]
        cyclone_category = label_encoder.inverse_transform([pred_encoded])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    return {
        "timestamp_utc": current_time,
        "location": {
            "latitude": lat,
            "longitude": lon,
            "district": location_name
        },
        "weather_data": {
            "usa_wind": usa_wind,
            "usa_pres": usa_pres,
            "storm_speed": storm_speed,
            "storm_dir": storm_dir,
            "month": month
        },
        "cyclone_condition": cyclone_category
    }
