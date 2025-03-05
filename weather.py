import requests
import json
import datetime

def get_date_tomorrow(): 
    in_a_day = datetime.datetime.today() + datetime.timedelta(days=1)
    tomorrow = in_a_day.date()
    return tomorrow

def search_by_city():
    search = str(input("Tast inn bynavn: "))
    user_agent = {'User-agent': 'Mozilla/5.0'}
    nominatim_url = f"https://nominatim.openstreetmap.org/search?q={search}&format=json"
    response = requests.get(nominatim_url, headers=user_agent)
    print(response.json()[0])
    if response.status_code == 200:

        if len(response.json()) > 0:
            city_data = response.json()[0]
        else:
            print(f"Feil: Kan ikke finne en by med navnet {search}. Vennligst kjør programmet på nytt.")
            exit()
    
    return city_data, search

def get_lat_lon_from_city_data(data: any) -> tuple[float, float]:
    latitude = float(data["lat"])
    longitude = float(data["lon"])

    shorten_lat = round(latitude, 2)
    shorten_lon = round(longitude, 2)

    float_lat = float(shorten_lat)
    float_lon = float(shorten_lon)

    return float_lat, float_lon

def get_weather_data(lat: float, lon: float) -> any:
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    #url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.91&lon=10.75"
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
    
    return data

def make_hours_tomorrow(tomorrow: str) -> tuple[list, list]:
    '''
    A function that creates and returns two lists.
    One containing the date+hourstrings needed for the ISO-format,
    and one formatted for the printout later.
    '''
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

def get_weather_data_for_tomorrow_per_hour(weather_data: any, hourstrings_iso: list) -> list:
    properties = weather_data["properties"]
    timeseries = properties["timeseries"]

    weather_data_per_hour = []
    for hours in range(0,48):
        hour = timeseries[hours]
        if hour["time"] in hourstrings_iso:
            weather_data_per_hour.append(timeseries[hours])
    return weather_data_per_hour

def get_temperatures_for_tomorrow(weather_data_per_hour: list) -> list:
    temperatures = []
    for hours in weather_data_per_hour:
        data = hours["data"]
        instant = data["instant"]
        details = instant["details"]
        temperature = details["air_temperature"]
        temperatures.append(temperature)
        
    return temperatures

def output_temperatures():
    tomorrow = get_date_tomorrow()
    city_data, search = search_by_city()
    lat, lon = get_lat_lon_from_city_data(city_data)
    weather_data = get_weather_data(lat, lon)
    hourstrings_iso, hourstrings = make_hours_tomorrow(str(tomorrow))
    weather_data_per_hour = get_weather_data_for_tomorrow_per_hour(weather_data, hourstrings_iso)
    temperatures = get_temperatures_for_tomorrow(weather_data_per_hour)

    print(f'Temperaturer for {search} {tomorrow.day}.{tomorrow.month}.{tomorrow.year}:')
    print('\n')
    for hour, temperature in zip(hourstrings, temperatures):
        outputstring = f'{hour} {temperature} grader'
        print(outputstring)

if __name__ == '__main__':
    output_temperatures()