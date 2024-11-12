# app.py
from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, app is running in Docker!"

# SMHI API URL
API_URL = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.0686/lat/59.3293/data.json"

def fetch_temperature():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Kasta fel om statuskod är inte 200
        data = response.json()
        
        # Extrahera temperaturen från API-svaret
        for timeseries in data.get('timeSeries', []):
            for param in timeseries['parameters']:
                if param['name'] == 't':  # 't' är för temperatur i Celsius
                    return timeseries['validTime'], param['values'][0]
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None

@app.route('/temperature', methods=['GET'])
def get_temperature():
    timestamp, temperature = fetch_temperature()
    if temperature is not None:
        return jsonify({
            'timestamp': timestamp,
            'temperature': temperature
        })
    else:
        return jsonify({'error': 'Could not fetch temperature data'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
