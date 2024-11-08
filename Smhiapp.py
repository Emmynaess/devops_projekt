import json
import pandas as pd
import requests
from datetime import datetime, timedelta

longitude = 18.063240
latitude = 59.334591

url = f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude:.6f}/lat/{latitude:.6f}/data.json'

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
                provider = 'SMHI'

                precipitation = "Yes" if precipitation > 0 else "No"

                weather_data.append({
                    'Created': current_time,
                    'Datum': datum,
                    'Hour': hour,
                    'Precipitation': precipitation,
                    'Provider': provider,
                })

        df = pd.DataFrame(weather_data)

        print(df)
    else:
        print(f'Error: {response.status_code}')


while True:
    print("Menu:")
    print("1. Hämta senaste data fÖr Stockholm")
    print("2. Avslut")

    choice = input("Välj ett alternativ: ")

    if choice == '1':
        fetch_weather_data()
    elif choice == '2':
        print("Avslutar programmet.")
        break
    else:
        print("Ogiltigt val. Välj ett giltigt alternativ (1, 2 eller 3).")
