import requests
import json
import datetime

def get_date_tomorrow(): 
    in_a_day = datetime.datetime.today() + datetime.timedelta(days=1)
    tomorrow = in_a_day.date()
    return tomorrow

def make_hours_tomorrow():
    tomorrow = str(get_date_tomorrow())
    hourstrings_iso = []
    hourstrings = []
    for hours in range(0,25):
        if hours > 9:
            hourstring_iso = f'{tomorrow}T{hours}:00:00Z'
            hourstring = f'Kl {hours}:00'
        else: 
            hourstring_iso = f'{tomorrow}T0{hours}:00:00Z'
            hourstring = f'Kl 0{hours}:00'
        hourstrings_iso.append(hourstring_iso)
        hourstrings.append(hourstring)

    return hourstrings_iso, hourstrings


def get_weather_data():
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75"
    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()
        properties = data["properties"]
        timeseries = properties["timeseries"]
        hourstrings_iso, hourstrings = make_hours_tomorrow()

        hours_iso = []
        for hours in range(0,48):
            hour = timeseries[hours]
            if hour["time"] in hourstrings_iso:
                hours_iso.append(timeseries[hours])

        temperatures = []
        for hours in hours_iso:
            data = hours["data"]
            instant = data["instant"]
            details = instant["details"]
            temperature = details["air_temperature"]
            temperatures.append(temperature)
          
        return temperatures
    
def output_temperatures():
    tomorrow = get_date_tomorrow()
    temperatures = get_weather_data()
    hourstrings_iso, hourstrings = make_hours_tomorrow()

    print(f'Temperaturer for Oslo {tomorrow.day}.{tomorrow.month}.{tomorrow.year}:')
    print('\n')
    for hour, temperature in zip(hourstrings, temperatures):
        outputstring = f'{hour} {temperature} grader'
        print(outputstring)
    

if __name__ == '__main__':
    output_temperatures()