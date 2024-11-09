from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, app is running in Docker!"

@app.route('/temperature')
def get_temperature():
    api_url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.0686/lat/59.3293/data.json"
    
    response = requests.get(api_url)
    data = response.json()
    
    temperature = data['timeSeries'][0]['parameters']
    temp_value = next(item['values'][0] for item in temperature if item["name"] == "t")
    
    return jsonify({"temperature": temp_value})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
