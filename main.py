
import timezonefinder
from datetime import datetime
import pytz
import argparse
import geocoder
import streamlit as st
import requests, json
import datetime
import pandas as pd
from IPython import get_ipython
import creds

def get_time_zone_by_location(longitude, latitude):
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=latitude, lng=longitude)
    if timezone_str is None:
        timezone_str = tf.closest_timezone_at(lat=latitude, lng=longitude)
    return timezone_str


def get_friendly_datetime(city_name, longitude, latitude):
    try:
        timezone_str = get_time_zone_by_location(longitude, latitude)
        user_timezone = pytz.timezone(timezone_str)

        utc_now = datetime.datetime.utcnow()

        local_time = utc_now.astimezone(user_timezone)

        formatted_time = local_time.strftime("%A, %B %d, %Y %I:%M %p")

        return (f"Current time in {city_name}: {formatted_time}")
    except pytz.UnknownTimeZoneError:
        return (f"Error: '{timezone_str}' is not a valid timezone.")

def get_local_time():
    local_date_time = None
    try:
        geo = geocoder.ip('me')
        if geo.current_result is not None:
            coordinates = geocoder.latlng
            if coordinates is not None:
                latitude, longitude = coordinates
                local_date_time = get_friendly_datetime(geo.current_result.address, longitude, latitude)
        return local_date_time
    except:
        return local_date_time

def get_city_wheather_info(city_name):
    api_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = api_url + "appid=" + creds.api_key + "&q=" + city_name + "&units=metric"
    if creds.api_key:
        response = requests.get(complete_url)
        json_file = response.json()
        if "cod" in json_file:
            return json_file
        else:
            return None

def check_streamlit():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if not get_script_run_ctx():
            use_streamlit = False
        else:
            use_streamlit = True
    except ModuleNotFoundError:
        use_streamlit = False
    return use_streamlit




use_cli=True
city_name=None
if 'google.colab' in str(get_ipython()) or check_streamlit():
  use_cli=False

if use_cli:
  parser = argparse.ArgumentParser(description='OpenWeatherMap CLI')
  parser.add_argument('--location', type=str, help='Location to get the weather for')
  args = parser.parse_args()

  if args.location:
    city_name = args.location

else:
    if 'google.colab' in str(get_ipython()):
        print("Weather Checker Application-Project(Asaf Levi)")
    elif check_streamlit():
        st.title("Weather Checker Application-Project(Asaf Levi)")
        df = pd.read_csv('https://raw.githubusercontent.com/datasets/world-cities/master/data/world-cities.csv')
    else:
        print("Weather Checker Application-Project(Asaf Levi)")


if not city_name:
    if 'google.colab' in str(get_ipython()):
        city_name = input("Enter city name: ")
    elif check_streamlit():
        df.columns =['City', 'Country', 'subcountry', 'geonameid']
        city_name = st.selectbox("Choose City:", df['City'].tolist())
    else:
        city_name = input("Enter city name: ")

wheather = get_city_wheather_info(city_name)

if wheather:
    if wheather["cod"] != "404":
        local_date_time = get_local_time()
        date_time = get_friendly_datetime(city_name, wheather['coord']['lon'], wheather['coord']['lat'])
        y = wheather["main"]
        current_temperature = y["temp"]
        fahrenheit_temperature = (current_temperature * 1.8) + 32
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = wheather["weather"]
        weather_description = z[0]["description"]
        print('Local Time : ', str(local_date_time))
        print(city_name + ' Time : ', str(date_time))
        print('--------------------------------', "")
        print('City : ', str(wheather["name"]))
        print('Country : ', str(wheather["sys"]["country"]))
        print('Weather Description : ', str(weather_description))
        print('Temperature (C/F) : ', str(current_temperature)+"/"+str(fahrenheit_temperature))
        print('atmospheric pressure (in hPa unit) : ', str(current_pressure))
        print('humidity (in percentage) : ', str(current_humidiy))
    else:
        print(f"{city_name} Not Found ")