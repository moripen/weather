import requests
import datetime


def get_dates_for_week() -> list: 
    dates_for_week = []
    for days in range(1,8):
        weekdays = datetime.datetime.today() + datetime.timedelta(days=days)
        dates_for_week.append(weekdays.date())
    return dates_for_week

def search_input():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    search = str(input("Tast inn bynavn: "))
    nominatim_url = f"https://nominatim.openstreetmap.org/search?q={search}&format=json"
    response = requests.get(nominatim_url, headers=user_agent)

    return response, search

def search_by_city() -> tuple[any, str]:
    response, search = search_input()
    city_data = 0
    if response.status_code == 200:
        while city_data == 0:
            if len(response.json()) > 0:
                city_data = response.json()[0]
            else:
                print(f"Feil: Kan ikke finne en by med navnet {search}. Vennligst prøv på nytt.")
                response, search = search_input()
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

def make_hourstring(date: str) -> list:
    hourstrings_iso = []
    for hours in range(0,25):
        if hours > 9:
            hourstring_iso = f'{date}T{hours}:00:00Z'
        else: 
            hourstring_iso = f'{date}T0{hours}:00:00Z'
        hourstrings_iso.append(hourstring_iso)

    return hourstrings_iso


def output_temperatures_for_week():
    city_data, search = search_by_city()
    dates_for_week = get_dates_for_week()
    lat, lon = get_lat_lon_from_city_data(city_data)
    weather_data = get_weather_data(lat, lon)

    print(dates_for_week, search, weather_data)


if __name__ == '__main__':
    output_temperatures_for_week()