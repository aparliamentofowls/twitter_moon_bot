import os
import requests
import datetime

VANCOUVER_LAT_LONG = "49.246292,-123.116226"
WEATHER_API_KEY = os.environ['API_KEY']
WEATHER_API_URL = 'http://api.weatherapi.com/v1/astronomy.json'


class MoonInfoObtainer:
    def __init__(self, city):
        self.city = city
        self.moonrise = "tbd"
        self.moonrise_year = datetime.datetime.now().year
        self.moonrise_month = datetime.datetime.now().strftime("%B")
        self.moonrise_day = datetime.datetime.now().day
        self.moonrise_hour = "tbd"
        self.moonrise_min = "tbd"
        self.moonrise_am_pm = "tbd"
        self.moon_phase = 'to be determined'
        self.tweet = 'to be determined'

    def obtain_moon_data(self):
        params = {
            "key": WEATHER_API_KEY,
            "q": VANCOUVER_LAT_LONG,
        }
        moon_data = requests.get(url=WEATHER_API_URL, params=params).json()
        self.moon_phase = moon_data['astronomy']['astro']['moon_phase']
        print(self.moon_phase)
        self.moonrise = moon_data['astronomy']['astro']['moonrise']
        print(self.moonrise)
        moonrise_hour = self.moonrise.split(":")[0]
        if moonrise_hour[0] == "0":
            moonrise_hour = moonrise_hour[1]
        self.moonrise_hour = moonrise_hour
        print(self.moonrise_hour)
        self.moonrise_min = self.moonrise.split(":")[1].split(" ")[0]
        print(self.moonrise_min)
        self.moonrise_am_pm = self.moonrise.split(":")[1].split(" ")[1]

    def formulate_tweet(self):
        self.tweet = f"The moon is rising in {self.city}!"

