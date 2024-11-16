from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

url = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.0686/lat/59.3293/data.json'

def fetch_weather_data():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = []
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for time_series in data['timeSeries']:
            timestamp_str = time_series['validTime'].replace('T', ' ').replace('Z', '')
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            time_diff_hours = (timestamp - datetime.now()).total_seconds() / 3600

            if 0 <= time_diff_hours <= 24:
                datum = timestamp_str.split()[0]
                hour = int(timestamp_str.split()[1][:2])
                precipitation = next(param['values'][0] for param in time_series['parameters'] if param['name'] == 'pcat')
                temperature = next(param['values'][0] for param in time_series['parameters'] if param['name'] == 't')
                provider = 'SMHI'
                precipitation = "Yes" if precipitation > 0 else "No"

                weather_data.append({
                    'Created': current_time,
                    'Datum': datum,
                    'Hour': hour,
                    'Precipitation': precipitation,
                    'Temperature': temperature,
                    'Provider': provider,
                })
        return weather_data
    else:
        return []


@app.route('/')
def display_weather():
    weather_data = fetch_weather_data()
    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)