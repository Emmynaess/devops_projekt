from flask import Flask
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def fetch_weather():
    location_name = "Stockholm"
    
    api_url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.0686/lat/59.3293/data.json"
    headers = {
        "Accept": "application/json",
        "User-Agent": "weather-app",
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        time_series = data["timeSeries"][0]
        parameters = time_series["parameters"]

        forecast_time = time_series["validTime"]
        forecast_time_formatted = datetime.strptime(forecast_time, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")

        weather = {}

        parameter_mapping = {
            "t": ("Temperature", "°C"),
            "ws": ("Wind Speed", "m/s"),
            "wd": ("Wind Direction", "degrees"),
            "r": ("Relative Humidity", "%"),
            "msl": ("Air Pressure", "hPa"),
            "vis": ("Visibility", "km"),
            "pmean": ("Mean Precipitation", "mm/h"),
            "pcat": ("Precipitation Category", ""),
        }

        for param in parameters:
            name = param["name"]
            if name in parameter_mapping:
                readable_name, unit = parameter_mapping[name]
                value = param["values"][0]
                if name == "pcat":
                    precipitation_types = {
                        0: "No precipitation",
                        1: "Snow",
                        2: "Snow and rain",
                        3: "Rain",
                        4: "Drizzle",
                        5: "Freezing rain",
                        6: "Freezing drizzle",
                    }
                    value = precipitation_types.get(value, "Unknown")
                    weather[readable_name] = value
                else:
                    weather[readable_name] = f"{value} {unit}"

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        result = f"""
        <h2>Current weather in {location_name}:</h2>
        <p><strong>Data fetched at:</strong> {current_time}</p>
        <p><strong>Forecast time:</strong> {forecast_time_formatted}</p>
        """
        for key, value in weather.items():
            result += f"<strong>{key}:</strong> {value}<br>"

        return result

    else:
        return "Failed to fetch data from SMHI API", response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
