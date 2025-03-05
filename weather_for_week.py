import requests
import datetime

def get_dates_weekday_for_week() -> tuple[list,list]: 
    dates_for_week = []
    weekdays_list = []
    for days in range(1,8):
        weekdays = datetime.datetime.today() + datetime.timedelta(days=days)
        dates_for_week.append(str(weekdays.date()))
        weekdays_list.append(weekdays.weekday())
    return dates_for_week, weekdays_list

def search_input():
    user_agent = {'User-agent': 'moripen/weather'}
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
        weather_data = response.json()
    
    return weather_data

def make_hourstring_for_week(dates_for_week: str) -> list:
    hourstrings_iso = []
    for date in dates_for_week:
        for hours in range(0,24):
            if hours > 9:
                hourstring_iso = f'{date}T{hours}:00:00Z'
            else: 
                hourstring_iso = f'{date}T0{hours}:00:00Z'
            hourstrings_iso.append(hourstring_iso)

    return hourstrings_iso

def get_weather_data_for_next_week_per_hour(weather_data: any, hourstrings_iso_week: list) -> list:
    properties = weather_data["properties"]
    timeseries = properties["timeseries"]
    weather_data_per_hour = []
    for hours in range(0,80):
        hour = timeseries[hours]
        if hour["time"] in hourstrings_iso_week:
            weather_data_per_hour.append(timeseries[hours])
    return weather_data_per_hour

def get_temperatures_for_next_week(weather_data_per_hour:list) -> list:
    temperatures = []
    for hours in weather_data_per_hour:
        data = hours["data"]
        instant = data["instant"]
        details = instant["details"]
        temperature = details["air_temperature"]
        temperatures.append([hours["time"], temperature])
        
    return temperatures

def separate_days(temperatures: list, dates_for_week: list):
    day1 = []
    day2 = []
    day3 = []
    day4 = []
    day5 = []
    day6 = []
    day7 = []
    for listentry in temperatures:
        if listentry[0].startswith(dates_for_week[0]):
            day1.append(listentry)
        elif listentry[0].startswith(dates_for_week[1]):
            day2.append(listentry)
        elif listentry[0].startswith(dates_for_week[2]):
            day3.append(listentry)
        elif listentry[0].startswith(dates_for_week[3]):
            day4.append(listentry)
        elif listentry[0].startswith(dates_for_week[4]):
            day5.append(listentry)
        elif listentry[0].startswith(dates_for_week[5]):
            day6.append(listentry)
        elif listentry[0].startswith(dates_for_week[6]):
            day7.append(listentry)

    return day1, day2, day3, day4, day5, day6, day7

def calculate_averages(day: list):
    sumtemp = 0.0
    sum_periods = [0.0, 0.0, 0.0, 0.0]
    n_in_period = [0, 0, 0, 0]
    for day in day:
        sumtemp += day[1]
        for i in range(0, 6):
            if f"T0{i}" in day[0]:
                sum_periods[0] += day[1]
                n_in_period[0] += 1
        for i in range(6, 12):
            if i > 9:
                if f"T{i}" in day[0]:
                    sum_periods[1] += day[1]
                    n_in_period[1] += 1
            else:
                if f"T0{i}" in day[0]:
                    sum_periods[1] += day[1]
                    n_in_period[1] += 1
        for i in range(12, 18):
            if f"T{i}" in day[0]:
                sum_periods[2] += day[1]
                n_in_period[2] += 1
        for i in range(18, 24):
            if f"T{i}" in day[0]:
                sum_periods[3] += day[1]
                n_in_period[3] += 1
    average_temp = round(sumtemp/len(day), 1)
    average_periods = [0,0,0,0]
    for i in range(0,4):
        average_periods[i] += round(sum_periods[i]/n_in_period[i],1)
    
    return average_temp, average_periods


def output_temperatures_for_week():
    city_data, search = search_by_city()
    lat, lon = get_lat_lon_from_city_data(city_data)
    weather_data = get_weather_data(lat, lon)
    dates_for_week, weekdays_list = get_dates_weekday_for_week()
    hourstrings_iso_week = make_hourstring_for_week(dates_for_week)
    weather_data_per_hour = get_weather_data_for_next_week_per_hour(weather_data, hourstrings_iso_week)
    temperatures_for_week = get_temperatures_for_next_week(weather_data_per_hour)
    day1, day2, day3, day4, day5, day6, day7 = separate_days(temperatures_for_week, dates_for_week)
    average_temp_day_1, average_periods_day1 = calculate_averages(day1)

if __name__ == '__main__':
    output_temperatures_for_week()