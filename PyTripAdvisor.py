from time import sleep
import os
import random
import sys

import sqlite3
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *

from bs4 import BeautifulSoup as bs

from webdriver_manager.chrome import ChromeDriverManager

import constants as const
from __init__ import __version__
from db import createDB

class PyTripAdvisor:
    def __init__(
        self,
        headless: bool = False):
        
        self.area = "g187791"
        self.url = const.BASE_URL % self.area
        self.headless = headless
        self.small_sleep = 3
        self.big_sleep = 10
        createDB()

        print(f"PyTripAdvisor Version: {__version__}")

    def getDriver(self):
        chrome_options = Options()
        chrome_options.add_argument(f"--lang=it")
        chrome_options.add_argument("start-maximized")
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        sleep(self.small_sleep)
        print("[i]\tDriver Accepted")
        return driver

    def getRestaurants(self, driver):
        """
        save restaurant's direct link
        """
        driver.get(self.url)
        sleep(self.small_sleep)
        driver.find_element(By.XPATH, "//button[text()='Accetto']").click()     #Accetta i cookie
        sleep(self.small_sleep)
        total_restaurants = int(driver.find_element(By.XPATH, "//span[@class='ffdhf b']").text.strip())
        pages = int(total_restaurants / 30)
        try:
            for page in range(1,pages+1):
                print(f"Getting page {page} / {pages}")
                soup = bs(driver.page_source, 'html.parser')
                container = driver.find_element(By.XPATH, ".//div[@data-test-target='restaurants-list']")
                for restaurant in container.find_elements(By.XPATH, "//div[@class='cauvp Gi o']"):
                    try:
                        url = restaurant.find_element(By.XPATH, ".//a[@class='bHGqj Cj b']").get_attribute("href")
                        name = restaurant.find_element(By.XPATH, ".//a[@class='bHGqj Cj b']").text
                        name = name[name.find('.')+1:].strip()
                        total_reviews = restaurant.find_element(By.XPATH, ".//span[@class='NoCoR']").text
                        try:
                            total_reviews = total_reviews[:total_reviews.find(' ')]
                            while '.' in total_reviews:
                                total_reviews = total_reviews.replace('.', '')
                            int(total_reviews)
                        except ValueError as er:
                            print(f'[!]\t{er}')
                            total_reviews = total_reviews[:total_reviews.find(' ')]

                        rating = bs(restaurant.find_element(By.XPATH, ".//span[@class='bFlvo']").get_attribute("innerHTML"), 'html.parser').find('svg')['aria-label']
                        rating = float(re.findall(r"[0-9]\,[0-9]", rating)[0].replace(',','.'))

                        more_infos = restaurant.find_elements(By.XPATH, ".//span[@class='ceUbJ']")
                        for info in more_infos:
                            if "€" in info.text and '-' in info.text:
                                price1,price2 = info.text.strip().split('-')
                                price = (price1.count('€')+price2.count('€'))/2
                            elif "€" in info.text:
                                price = info.text.strip().count('€')

                        # add to DB
                        conn = sqlite3.connect(f'{const.DB_NAME}')
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO restaurants VALUES (?, ?, ?, ?, ?, ?)",
                        (None,
                        url,
                        name,
                        rating,
                        total_reviews,
                        price))
                        conn.commit()

                    except NoSuchElementException as er:
                        print(f'[!]\t{er}')
                        pass
                    
                next_page = soup.find("a", {"class": "next"})
                driver.get(self.url + next_page.attrs["href"])
                sleep(self.small_sleep-1.5)    
        except KeyboardInterrupt:
            driver.close()
            sys.exit()

        conn.close()  
        return None



if __name__ == "__main__":
    Bot = PyTripAdvisor()
    driver = Bot.getDriver()
    Bot.getRestaurants(driver)
    
    

