import requests
import pprint
import json
import pandas as pd
def create_openweather_string(lat,lon,appid="ba8851cba967f520b368030ae5332069"):
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}"
    return URL
def get_openweather(lat,lon,appid="ba8851cba967f520b368030ae5332069"):
    return requests.get(create_openweather_string(lat, lon, appid))


def log_file():
    x= get_openweather(12,52)
    print(x.text)
    mydict = json.loads(x.text)
    pprint.pprint(mydict)
    with open("weather.log","w") as log:
        log.write(x)