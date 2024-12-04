from flask import Flask, jsonify
import requests

app = Flask(__name__)

def fetch_temperature(data):
    """
    Extracts the temperature from SMHI API response.
    """
    time_series = data.get("timeSeries", [])
    if time_series:
        parameters = time_series[0].get("parameters", [])
        for param in parameters:
            if param["name"] == "t": 
                return f"{param['values'][0]} C"
    return None

@app.route("/")
def fetch_weather():
    """
    Fetches temperature for Stockholm.
    """ ####
    api_url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.0686/lat/59.3293/data.json"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Temp-app", ###weather
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        temperature = fetch_temperature(data)

        if temperature:
            return f"""
            <html>
                <head><title>Tempperature in Stockholm</title></head>
                <body>
                    <h2><strong>Tempperature in Stockholm</strong></h2>
                    <p><strong>Temperature:</strong> {temperature}</p>
                </body>
            </html>
            """ ####
        else:
            return """
            <html>
                <head><title>Tempperature in Stockholm</title></head>
                <body>
                    <h2><strong>Tempperature in Stockholm</strong></h2>
                    <p><strong>Temperature data is not available.</strong></p>
                </body>
            </html>
            """ ###
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data from SMHI API", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
