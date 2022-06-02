from time import sleep
import os
import time
import sys
import datetime as dt
import locale

#import sqlite3
import mysql.connector #mysql-connector-python
import re

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from concurrent.futures import ProcessPoolExecutor

from bs4 import BeautifulSoup as bs

from webdriver_manager.chrome import ChromeDriverManager

import constants as const
from __init__ import __version__
from db import db_connect

locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")       #in linux use this: "it_IT.UTF-8"

class PyTripAdvisor:
    def __init__(
        self,
        headless: bool = False):
        
        self.area = "g187791"
        #self.url = const.BASE_URL % self.area
        self.url = const.BASE_URL
        self.headless = headless
        self.small_sleep = 3
        self.big_sleep = 10
        #createDB()
        #exportSchema()
        self.conn, self.cursor = db_connect()

        print(f"PyTripAdvisor Version: {__version__}")
    
    @staticmethod
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

            
    def user_exist(self, user):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM reviewers WHERE reviewer_name=%s)", (user,))
        self.conn.commit()
        result = self.cursor.fetchall()
        if result[0][0]:
            return True
        return False

    def restaurant_exist(self, url):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM restaurants WHERE restaurant_url=%s)", (url,))
        result = self.cursor.fetchall()
        if result[0][0]:
            return True
        return False
        

    def review_exist(self, url):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM reviews WHERE review_url=%s)", (url,))
        self.conn.commit()
        result = self.cursor.fetchall()
        if result[0][0]:
            return True
        return False

    def getDriver(self):
        locale = "it"
        chrome_options = Options()
        chrome_options.add_argument(f"--lang={locale}")
        chrome_options.add_argument("start-maximized")
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--incognito")
        #chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        sleep(self.small_sleep)
        print("[i]\tDriver Accepted")
        return driver

    def search(self, driver):
        driver.get(self.url)
        sleep(2)
        driver.find_element(By.XPATH, "//button[text()='Accetto']").click()     #Accetta i cookie
        sleep(self.small_sleep)
        driver.find_elements(By.XPATH, "//div[@class='dyTIx eMorU elMNN gayuF dWGsc ecxqv']")[3].click()
        sleep(1)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//form[@class='bmTdH o']//input[@title='Cerca']")))
        actionChains = ActionChains(driver)
        actionChains.move_to_element(element).click().perform()
        sleep(.5)
        actionChains.move_to_element(element).send_keys("Roma").perform()
        sleep(.5)
        actionChains.move_to_element(element).send_keys(Keys.ENTER).perform()
        sleep(5)

    def start_page(self, driver, page_num):
        driver.get(f"{const.BASE_URL}/RestaurantSearch-g187791-oa{page_num*30}-a_date.2022__2D__06__2D__02-a_people.2-a_time.20%3A00%3A00-a_zur.2022__5F__06__5F__02-Rome_L.html#EATERY_LIST_CONTENTS")
        sleep(self.small_sleep)
        driver.find_element(By.XPATH, "//button[text()='Accetto']").click()     #Accetta i cookie
        sleep(self.small_sleep)
        next = driver.find_element(By.XPATH, "//div[@class='unified pagination js_pageLinks']/a[contains(text(),'Avanti')]")
        actionChains = ActionChains(driver)
        actionChains.move_to_element(next).perform()
        sleep(.5)
        next.click()
        sleep(2)

    def getRestaurants(self, driver, page_num=0):
        total_restaurants = int(driver.find_element(By.XPATH, ".//span[@class='ffdhf b']").text.strip())
        pages = int(total_restaurants / 30)
        actionChains = ActionChains(driver)
        try:
            for page in range(1+page_num,pages+1):
                print(f"Getting page {page} / {pages}")
                sleep(1)
                container = driver.find_element(By.XPATH, "//div[@data-test-target='restaurants-list']")
                actionChains.move_to_element(container).perform()
                sleep(.15)
                for restaurant in container.find_elements(By.XPATH, ".//div[@class='cauvp Gi o']"):
                    try:
                        url_name = restaurant.find_element(By.XPATH, ".//a[@class='bHGqj Cj b']")
                        url = url_name.get_attribute("href")
                        name = url_name.text
                        name = name[name.find('.')+1:].strip()
                        total_reviews = restaurant.find_element(By.XPATH, ".//span[@class='NoCoR']").text
                        try:
                            total_reviews = total_reviews[:total_reviews.find(' ')]
                            while '.' in total_reviews:
                                total_reviews = total_reviews.replace('.', '')
                            total_reviews = int(total_reviews)
                        except ValueError as er:
                            print(f'[!]\t{er}')
                            total_reviews = total_reviews[:total_reviews.find(' ')]
                        
                        if total_reviews < 50:
                            continue

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
                        if not self.restaurant_exist(url):
                            self.cursor.execute("INSERT INTO restaurants VALUES (%s, %s, %s, %s, %s, %s)",
                            (url,
                            name,
                            rating,
                            total_reviews,
                            price,
                            None))
                            self.conn.commit()

                    except Exception as er:
                        print(f'[!]\t{er}')
                        continue
                
                next = driver.find_element(By.XPATH, "//div[@class='unified pagination js_pageLinks']/a[contains(text(),'Avanti')]")
                actionChains.move_to_element(next).perform()
                sleep(.5)
                next.click()
                sleep(1.5)
        except KeyboardInterrupt:
            driver.close()
            print("[i]\texits gracefully 1")
            sys.exit()

        self.cursor.close()  
        return None


    def restaurantUrls(self):
        self.cursor.execute("SELECT restaurant_url FROM restaurants")
        rows = self.cursor.fetchall()
        rows = [x[0] for x in rows]
        self.conn.commit()
        self.cursor.close()
        return rows

    def getReviews(self, restaurant_url):
        driver = self.getDriver()
        driver.get(restaurant_url)
        #sleep(self.small_sleep)
        sleep(3)
        start = time.perf_counter()
        try:
            try:
                driver.find_element(By.XPATH, "//button[text()='Accetto']").click()     #Accetta i cookie
                sleep(1)
            except Exception as e:
                pass

            try: 
                restaurant_address = driver.find_element(By.XPATH, "//span[@class='brMTW']").text
            except Exception as e:
                restaurant_address = None
            try:
                total_reviews = driver.find_element(By.XPATH, "//span[@class='count']").text
                total_reviews = re.findall(r"\d+", total_reviews)
                if len(total_reviews) > 1:
                    total_reviews = int(f"{total_reviews[0]}{total_reviews[1]}")
                elif len(total_reviews) == 1:
                    total_reviews = int(total_reviews[0])
            except Exception as e:
                total_reviews = 0

            pages = int(total_reviews / 10)
            if pages > 20: 
                pages = 20 # max 200 per restaurant

            for page in range(0,pages):
                print(f"[i] Getting page {page} / {pages}")
                try:
                    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='taLnk ulBlueLinks']"))).click()
                    sleep(1)
                except Exception as e:
                    pass
                
                container = driver.find_elements(By.XPATH, "//div[@class='review-container']")
                actions = ActionChains(driver)

                try:
                    actions.move_to_element(container[0]).perform()
                except Exception as e:
                    pass

                for i in range(0, len(container)):
                    # if exists, skip
                    review_url = container[i].find_element(By.XPATH, ".//a[@class='title ']").get_attribute("href")
                    if self.review_exist(review_url):
                        stop = time.perf_counter()
                        print(f"[i] page n°{page} took {stop - start:0.4f} seconds")
                        continue

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

                    try:
                        title = container[i].find_element(By.XPATH, ".//span[@class='noQuotes']").text
                    except Exception as e:
                        title = None

                    try:
                        visit_date = container[i].find_element(By.XPATH, ".//div[@data-prwidget-name='reviews_stay_date_hsx']").text
                        visit_date = visit_date.replace("Data della visita: ", "")
                        visit_date = dt.datetime.strptime(visit_date, "%B %Y")
                    except Exception as e:
                        visit_date = None

                    try:
                        review_text = container[i].find_element(By.XPATH, ".//p[@class='partial_entry']").text.replace("\n", " ")
                    except Exception as e:
                        review_text = None

                    try:
                        helpful = container[i].find_element(By.XPATH, ".//span[@class='numHelp ']").text
                        if len(helpful) == 0:
                            helpful = 0
                    except Exception as e:
                        helpful = 0

                    ################################### REVIEWER SECTION #####################################
                    # if exists, skip
                    member_info = container[i].find_element(By.XPATH, ".//div[@class='member_info']")
                    username = member_info.find_element(By.XPATH, ".//div[@class='info_text pointer_cursor']/div").text
                    if self.user_exist(username):
                        stop = time.perf_counter()
                        print(f"[i] page n°{page} took {stop - start:0.4f} seconds")
                        continue
                    

                    actions.move_to_element(container[i].find_element(By.XPATH, ".//span[@class='noQuotes']")).perform()
                    sleep(0.75)
                    avatar = WebDriverWait(container[i], 10).until(EC.element_to_be_clickable((By.XPATH, ".//div[contains(@class, 'ui_avatar resp')]")))
                    avatar.click()
                    sleep(0.75)
                    
                    reviewer_box = WebDriverWait(container[i], 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'memberOverlayRedesign g10n')]/a")))
                    
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

                            home = home.lower().strip()
                            if ',' in home:
                                home = re.findall(r"da ([\w ]*),", home)[0]
                            else:
                                home = re.findall(r"(\w+)$", home)[0]
                            home = home.title()
                        else:
                            user_since = profile_info.replace("Utente di Tripadvisor da ", "")
                            user_since = dt.datetime.strptime(user_since, "%b %Y")
                            home = None

                    except Exception as e:
                        print(f"[!]\t{e.with_traceback()}")
                        user_since = None
                        home = None

                    # add to DB
                    if not self.review_exist(url=review_url):
                        self.cursor.execute("INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (review_url,
                        restaurant_url,
                        reviewer_name,
                        title,
                        date_r,
                        visit_date,
                        rating,
                        helpful,
                        device,
                        review_text
                        ))
                        self.conn.commit()

                    if not self.user_exist(user=reviewer_name):
                        self.cursor.execute("INSERT INTO reviewers VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (reviewer_name,
                        profile_link,
                        contributes,
                        level,
                        user_since,
                        home,
                        cities,
                        helpfuls
                        ))
                        self.conn.commit()
                        self.cursor.close()

                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@class='ui_overlay ui_popover arrow_left ']/div[@class='ui_close_x']"))
                        ).click()

                    sleep(.5)

                stop = time.perf_counter()
                print(f"[i] page n°{page} took {stop - start:0.4f} seconds")
                
                try:
                    next = driver.find_element(By.XPATH, "//div[@class='unified ui_pagination ']/a[contains(text(),'Avanti')]")
                    actionChains = ActionChains(driver)
                    actionChains.move_to_element(next).perform()
                    sleep(.75)
                    next.click()
                except Exception as e:
                    print(e.with_traceback())
                    break
                sleep(.5)
                
            self.cursor.execute("UPDATE restaurants SET address=%s WHERE restaurant_url=%s", (restaurant_address,restaurant_url))
            self.conn.commit()
            self.cursor.close()
        except KeyboardInterrupt:
            driver.quit()
            print("[i]\texits gracefully")
            sys.exit()
        driver.quit()
        return


if __name__ == "__main__":
    Bot = PyTripAdvisor()
    Bot.clear()
    #Bot.user_exist('pippo')
    driver = Bot.getDriver()
    #try:
    Bot.search(driver)
    #Bot.start_page(driver,page_num=89)
    Bot.getRestaurants(driver,page_num=0)
    #urls = Bot.restaurantUrls()
    #drivers = [Bot.getDriver() for i in range(4)]
    #with ProcessPoolExecutor(max_workers=4) as executor:
    #    result = [executor.map(Bot.getReviews, urls)]

    #Bot.getReviews(driver, urls)
    """except Exception as er:
        print(f"[!]\t{er.with_traceback()}")
        #driver.close()
        print("[i]\texits gracefully 2")
        sys.exit()"""