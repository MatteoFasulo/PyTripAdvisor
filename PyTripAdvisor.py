from time import sleep
import os
import random
import sys
import datetime as dt
import locale

import sqlite3
import re

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
from db import createDB, exportSchema

locale.setlocale(locale.LC_TIME, "it_IT")

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
        exportSchema()

        print(f"PyTripAdvisor Version: {__version__}")
    
    @staticmethod
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

            
    @staticmethod
    def user_exist(user):
        conn = sqlite3.connect(f'{const.DB_NAME}')
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM reviewers WHERE reviewer_name=?)", (user,))
        conn.commit()
        result = cursor.fetchall()
        if result[0][0]:
            return True
        return False

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
            print("[i]\texits gracefully")
            sys.exit()

        conn.close()  
        return None


    def restaurantUrls(self):
        conn = sqlite3.connect(f'{const.DB_NAME}')
        conn.row_factory = lambda cursor, row: row[0] # workaround for tuple return of fetchall in sql
        cursor = conn.cursor()
        cursor.execute("SELECT restaurant_url FROM restaurants")
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows

    def getReviews(self, driver, urls):
        
        for restaurant_url in urls:
            driver.get(restaurant_url)
            sleep(self.small_sleep)
            try:
                try:
                    driver.find_element(By.XPATH, "//button[text()='Accetto']").click()     #Accetta i cookie
                    sleep(1)
                except Exception as e:
                    pass

                try: 
                    restaurant_address = driver.find_element(By.XPATH, ".//span[@class='brMTW']").text
                except Exception as e:
                    restaurant_address = None
                try:
                    total_reviews = driver.find_element(By.XPATH, ".//span[@class='count']").text
                    total_reviews = re.findall(r"\d+", total_reviews)
                    if len(total_reviews) > 1:
                        total_reviews = int(f"{total_reviews[0]}{total_reviews[1]}")
                    elif len(total_reviews) == 1:
                        total_reviews = int(total_reviews[0])
                except Exception as e:
                    total_reviews = 0
                    continue

                if total_reviews < 10:
                    continue

                pages = int(total_reviews / 10)

                for page in range(0,pages):
                    print(f"[i] Getting page {page} / {pages}")
                    sleep(0.5)
                    soup = bs(driver.page_source, 'html.parser')
                    try:
                        driver.find_element(By.XPATH, ".//span[@class='taLnk ulBlueLinks']").click()
                        sleep(1)
                    except Exception as e:
                        pass
                    
                    container = driver.find_elements(By.XPATH, ".//div[@class='review-container']")
                    actions = ActionChains(driver)

                    try:
                        actions.move_to_element(container[1]).perform()
                    except Exception as e:
                        actions.move_to_element(container[0]).perform()

                    for i in range(0, len(container)):
                        """
                        if i == 0:
                            
                        else:
                            actions.move_to_element(container[i+1]).perform()"""
                        review_url = container[i].find_element(By.XPATH, ".//a[@class='title ']").get_attribute("href")

                        rating = container[i].find_element(By.XPATH, ".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
                        rating = int(rating)
                        rating = rating/10

                        date_r = container[i].find_element(By.XPATH, ".//span[contains(@class, 'ratingDate')]").get_attribute("title")
                        date_r = dt.datetime.strptime(date_r, "%d %B %Y")

                        try:
                            device = container[i].find_element(By.XPATH, ".//span[@class='viaMobile']")
                            device = device.text
                        except Exception as e:
                            device = None

                        title = container[i].find_element(By.XPATH, ".//span[@class='noQuotes']").text

                        visit_date = container[i].find_element(By.XPATH, ".//div[@data-prwidget-name='reviews_stay_date_hsx']").text
                        visit_date = visit_date.replace("Data della visita: ", "")
                        visit_date = dt.datetime.strptime(visit_date, "%B %Y")

                        review_text = container[i].find_element(By.XPATH, ".//p[@class='partial_entry']").text.replace("\n", " ")

                        try:
                            helpful = container[i].find_element(By.XPATH, ".//span[@class='numHelp ']").text
                            if len(helpful) == 0:
                                helpful = 0
                        except Exception as e:
                            helpful = 0

                        ########################################################################

                        avatars = container[i].find_elements(By.XPATH, "//div[contains(@class, 'ui_avatar resp')]")
                        #actions.move_to_element(avatars[i]).perform()
                        sleep(0.75)
                        avatars[i].click()
                        sleep(0.75)

                        reviewer_box = container[i].find_element(By.XPATH, "//div[contains(@class, 'memberOverlayRedesign g10n')]/a")
                        reviewer_name = reviewer_box.get_attribute('href').split(sep="/")[-1]

                        profile_link = reviewer_box.get_attribute('href')

                        try:
                            level = bs(reviewer_box.find_element(By.XPATH, "//div[@class='badgeinfo']").get_attribute('innerHTML'), 'html.parser').find('span').text.strip()
                            level = int(level)
                        except Exception as e:
                            level = None
                        
                        informations = reviewer_box.find_elements(By.XPATH, "//span[@class='badgeTextReviewEnhancements']")
                        try:
                            contributes = informations[0].text
                            contributes = re.findall(r"\d+",contributes)[0]
                        except Exception as e:
                            contributes = None
                        try:
                            cities = informations[1].text
                            cities = re.findall(r"\d+",cities)[0]
                        except Exception as e:
                            cities = None
                        try:
                            helpfuls = informations[2].text
                            helpfuls = re.findall(r"\d+",helpfuls)[0]
                        except Exception as e:
                            helpfuls = None
                        
                        try:
                            profile_info = reviewer_box.find_elements(By.XPATH, "//ul[@class='memberdescriptionReviewEnhancements']")[0].text

                            if '\n' in profile_info:
                                user_since, home = profile_info.split(sep="\n")
                                user_since = user_since.replace("Utente di Tripadvisor da ", "")
                                user_since = dt.datetime.strptime(user_since, "%b %Y")

                                home = home.lower()
                                home = re.findall(r"da ([\w ]*),", home)[0]
                                home = home.title()
                            else:
                                user_since = profile_info.replace("Utente di Tripadvisor da ", "")
                                user_since = dt.datetime.strptime(user_since, "%b %Y")
                                home = None

                        except Exception as e:
                            print(f"[!]\t{e}")
                            user_since = None
                            home = None

                        # add to DB
                        conn = sqlite3.connect(f'{const.DB_NAME}')
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (None,
                        restaurant_url,
                        reviewer_name,
                        title,
                        date_r,
                        visit_date,
                        rating,
                        helpful,
                        device,
                        review_text,
                        review_url
                        ))
                        conn.commit()

                        if not self.user_exist(user=reviewer_name):
                            cursor.execute("INSERT INTO reviewers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (reviewer_name,
                            profile_link,
                            contributes,
                            level,
                            user_since,
                            home,
                            cities,
                            helpfuls
                            ))
                            conn.commit()
                        conn.close()

                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[@class='ui_overlay ui_popover arrow_left ']/div[@class='ui_close_x']"))
                            ).click()

                        sleep(0.25)
                    
                    next_page = soup.find("a", {"class": "next"})
                    try:
                        driver.get(restaurant_url + next_page.attrs["href"])
                        sleep(self.small_sleep)
                    except Exception as e: # disabled button
                        break
                    
                #TODO: spostare questo fuori dal ciclo for delle pagine reviews
                conn = sqlite3.connect(f'{const.DB_NAME}')
                cursor = conn.cursor()
                cursor.execute("UPDATE restaurants SET address=? WHERE restaurant_url=?", (restaurant_address,restaurant_url))
                conn.commit()
            except KeyboardInterrupt:
                driver.close()
                print("[i]\texits gracefully")
                sys.exit()
        return



if __name__ == "__main__":
    Bot = PyTripAdvisor()
    Bot.clear()
    driver = Bot.getDriver()
    #Bot.getRestaurants(driver)
    urls = Bot.restaurantUrls()
    Bot.getReviews(driver, urls)
    driver.close()
    
    

