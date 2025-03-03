import requests
import json

def get_weather_data():
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75"
    response = requests.get(url)
    print(response.status_code)
    #check response ok
    if response.status_code == 200:

        data = response.json()
        properties = data["properties"]
        timeseries = properties["timeseries"]
        for hours in range(12,37):
            time = []
            time.append(timeseries[hours])
        return time
    
    
data = get_weather_data()
print(data)