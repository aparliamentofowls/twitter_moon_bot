import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import mooninfo_obtainer
import time

# Constants - Selenium Related
CHROME_DRIVER_PATH = os.environ["CDPATH"]
TWITTER_URL = "https://twitter.com/i/flow/login"
TWITTER_PASSWORD = os.environ["TWPASSWORD"]
TWITTER_EMAIL = os.environ['TWEMAIL']
TWITTER_USERNAME = os.environ['TWUSERNAME']

class MoonriseMoonsetBot:
    def __init__(self):
        service = Service(executable_path=CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=service)

    def sign_in_to_twitter(self, myApiBot):
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
        self.tweet_moon_info(wait, myApiBot)

    def find_element_send_keys(self, wait, xpath, key):
        selector = wait.until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        selector.send_keys(key)
        selector.send_keys(Keys.RETURN)

    def tweet_moon_info(self, wait, myApiBot):
        schedule_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="scheduleOption"]')))
        schedule_button.click()

        self.find_element_send_keys(wait, '//select[@id="SELECTOR_6"]', myApiBot.moonrise_am_pm)
        time.sleep(2)
        self.find_element_send_keys(wait, '//select[@id="SELECTOR_1"]', myApiBot.moonrise_month)
        time.sleep(2)
        self.find_element_send_keys(wait, '//select[@id="SELECTOR_2"]', myApiBot.moonrise_day)
        time.sleep(2)
        self.find_element_send_keys(wait, '//select[@id="SELECTOR_3"]', myApiBot.moonrise_year)
        time.sleep(2)
        self.find_element_send_keys(wait, '//select[@id="SELECTOR_4"]', myApiBot.moonrise_hour)
        time.sleep(2)
        self.find_element_send_keys(wait, '//select[@id="SELECTOR_5"]', myApiBot.moonrise_min)
        time.sleep(2)

        confirm_button = wait.until(
           EC.visibility_of_element_located((By.XPATH, '//div[@data-testid="scheduledConfirmationPrimaryAction"]')))
        confirm_button.click()

        tweet_textbox = wait.until(
           EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'public-DraftStyleDefault-block')]")))
        tweet_textbox.send_keys(myApiBot.tweet)

        emoji_selector = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Add emoji"]')))
        emoji_selector.click()

        emoji_search = wait.until(
           EC.visibility_of_element_located((By.XPATH, '//input[@aria-label="Search emojis"]'))
        )
        emoji_search.click()
        emoji_search.send_keys(myApiBot.moon_phase)

        first_result = wait.until(
           EC.visibility_of_element_located((By.XPATH, '//*[@id="emoji_picker_categories_dom_id"]/div/div[1]/div/div[2]'
                                                       '/div/div/div[1]')))
        first_result.click()

        outside_area = wait.until(
           EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div[1]')))
        outside_area.click()

        tweet_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButtonInline"]')))
        tweet_button.click()


myApiBot = mooninfo_obtainer.MoonInfoObtainer("vancouver")
myApiBot.obtain_moon_data()
myApiBot.formulate_tweet()

myMoonBot = MoonriseMoonsetBot()
myMoonBot.sign_in_to_twitter(myApiBot)
time.sleep(10)
myMoonBot.driver.close()