import requests
import datetime
import twilio.rest
from pytz import timezone
from twilio.rest import Client

API_KEY = "YOUR OPEN WEATHER MAP API KEY"
ACCOUNT_SID = 'YOUR TWILIO ACCOUNT SID'
AUTH_TOKEN = 'YOUR TWILIO AUTH TOKEN '

# example with lat and lon -
# https: // api.openweathermap.org / data / 2.5 / forecast?lat = 37.931961 & lon = -121.695930 & appid = 1176e9ae092df65480e70f96400cb3a6
# https://api.openweathermap.org/data/3.0/onecall?lat=37.931961&lon=-121.695930&appid=1176e9ae092df65480e70f96400cb3a6&units=imperial

WEATHER_SITE = "https://api.openweathermap.org/data/3.0/onecall"
LAT = 'YourLatitude'
LON = 'YourLongitude'

parameters = {
    'lat': LAT,
    'lon': LON,
    'appid': API_KEY,
    'units': 'imperial',
    "exclude": "current,minutely,daily"
}


def get_weather():
    requesting = requests.get(url=WEATHER_SITE, params=parameters)
    requesting.raise_for_status()
    data = requesting.json()
    return data

def get_umbrell(weather_report):
    weather_slice = weather_report["hourly"][:11]
    umbrella = []
    for x in weather_slice:
        if (x['weather'][0]['id'] < 700):
            local_time = datetime.datetime.fromtimestamp(x['dt'])
            local_time = timezone('US/Pacific').localize(local_time)
            umbrella.append(f"Date: {local_time.strftime('%m/%d/%Y %H:%M:%S %Z')} - Bring An Umbrella !")
            my_twillio = twilio.rest.Client(ACCOUNT_SID, AUTH_TOKEN)
            message = my_twillio.messages.create(body=f"Date: {local_time.strftime('%m/%d/%Y %H:%M:%S %Z')} - Bring An Umbrella !",
                                                 from_='TWILIO PHONE NUMBER OR SOMETHING ELSE',
                                                 to='PHONE NUMBER TO SEND IT TO')
            print(message.status)

my_weather = get_weather()
get_umbrell(my_weather)
