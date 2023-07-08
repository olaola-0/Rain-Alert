import requests
from twilio.rest import Client
import os

api_key = os.environ.get("OWM_API_KEY")
MY_LAT = "Location Latitude"  #Float
MY_LON = "Location Longitude"  #Float
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.8/onecall"

account_sid = os.environ.get("ACCOUNT_SSID")
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": api_key,
    "units": "metric",
    "exclude": "current,minutely,daily",
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

hourly = weather_data["hourly"]
# weather_hourly = []
# for i in range(12):
#    weather_hourly.append(hourly[i]["weather"][0]["id"])

# Slice the Hourly forecast and return the first 12 hours forecast
weather_slice = hourly[:12]

will_it_rain = False

for hour in weather_slice:
    # find condition code in first 12 hours of Hourly
    weather_condition_code = hour["weather"][0]["id"]
    # Convert the returned weather
    if int(weather_condition_code) < 700:
        will_it_rain = True

# if weather condition code is < 700, advise to bring umbrella
if will_it_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It looks like it will be a wet 💦 day. Bring an umbrella ☔",
        from_=os.environ.get("FROM_NUMBER"),
        to=os.environ.get("TO_NUMBER")
    )
    print(message.status)