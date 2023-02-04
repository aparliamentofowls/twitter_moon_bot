import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Constants - Selenium Related
CHROME_DRIVER_PATH = os.environ["CDPATH"]
TWITTER_URL = "https://twitter.com/i/flow/login"
TWITTER_PASSWORD = os.environ["TWPASSWORD"]
TWITTER_EMAIL = os.environ['TWEMAIL']
TWITTER_USERNAME = os.environ['TWUSERNAME']

# Constants - Weather Api Related
VANCOUVER_LAT_LONG = "49.246292,-123.116226"
WEATHER_API_KEY = os.environ['API_KEY']
WEATHER_API_URL = 'http://api.weatherapi.com/v1/astronomy.json'


class MoonriseMoonsetBot:
    def __init__(self):
        service = Service(executable_path=CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service)

    def sign_in_to_twitter(self):
        self.driver.get(TWITTER_URL)
        wait = WebDriverWait(self.driver, 20)
        email_textfield = wait.until(EC.element_to_be_clickable((By.NAME, "text")))
        email_textfield.send_keys(TWITTER_EMAIL)
        email_textfield.send_keys(Keys.RETURN)
        try:
            sus_username_input = wait.until(EC.element_to_be_clickable((By.NAME, "text")))
            sus_username_input.send_keys(TWITTER_USERNAME)
            sus_username_input.send_keys(Keys.RETURN)
        except TimeoutException:
            pass
        password_textfield = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        password_textfield.send_keys(TWITTER_PASSWORD)
        password_textfield.send_keys(Keys.RETURN)

    def retrieve_moon_info(self):
        params = {
            "key": WEATHER_API_KEY,
            "q": VANCOUVER_LAT_LONG,
        }
        moon_data = requests.get(url=WEATHER_API_URL, params=params).json()
        moon_phase = moon_data['astronomy']['astro']['moon_phase']
        print(moon_phase)
        moonrise = moon_data['astronomy']['astro']['moonrise']
        print(moonrise)


myMoonBot = MoonriseMoonsetBot()
myMoonBot.retrieve_moon_info()
myMoonBot.sign_in_to_twitter()
time.sleep(10)
myMoonBot.driver.close()
