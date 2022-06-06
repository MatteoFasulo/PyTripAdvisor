from time import sleep
import os
import time
import datetime as dt
import locale
import re

import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

from webdriver_manager.chrome import ChromeDriverManager

from concurrent.futures import ProcessPoolExecutor

from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image

import constants as const
from __init__ import __version__
from db import db_connect

############################################################################################
locale.setlocale(locale.LC_TIME, "it_IT")       #in linux use this: "it_IT.UTF-8"

class PyTripAdvisor:
    def __init__(
        self,
        headless: bool = False):
        
        self.area = "g187791"
        self.url = const.BASE_URL
        self.headless = headless
        self.small_sleep = 3
        self.big_sleep = 10
        #createDB()
        #exportSchema()

        print(f"PyTripAdvisor Version: {__version__}")
    
    @staticmethod
    def clear():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def user_exist(user):
        conn, cursor = db_connect()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM reviewers WHERE reviewer_name=%s)", (user,))
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        if result[0][0]:
            return True
        return False

    @staticmethod
    def restaurant_exist(url):
        conn, cursor = db_connect()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM restaurants WHERE restaurant_url=%s)", (url,))
        result = cursor.fetchall()
        conn.close()
        if result[0][0]:
            return True
        return False
    
    @staticmethod
    def restaurant_cuisine_exist(url):
        conn, cursor = db_connect()
        cursor.execute("SELECT cuisine FROM restaurants WHERE restaurant_url = %s", (url,))
        result = cursor.fetchall()
        conn.close()
        if result[0][0] == None:
            return False
        return True
        
    @staticmethod
    def review_exist(url):
        conn, cursor = db_connect()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM reviews WHERE review_url=%s)", (url,))
        conn.commit()
        result = cursor.fetchall()
        conn.close()
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
        chrome_prefs = {}
        #chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        chrome_options.add_experimental_option('prefs', chrome_prefs)
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        sleep(self.small_sleep)
        return driver

    def search(self, driver):
        driver.get(self.url)
        sleep(2)
        driver.find_element(By.XPATH, "//button[text()='Accetto']").click()     #Accetta i cookie
        sleep(self.small_sleep)
        driver.find_elements(By.XPATH, "//div[@class='dyTIx eMorU elMNN gayuF dWGsc ecxqv']")[3].click()
        sleep(1)
        element = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//form[@class='bmTdH o']//input[@title='Cerca']")))
        actionChains = ActionChains(driver)
        actionChains.move_to_element(element).click().perform()
        sleep(.5)
        actionChains.move_to_element(element).send_keys("Roma").perform()
        sleep(.5)
        actionChains.move_to_element(element).send_keys(Keys.ENTER).perform()
        sleep(5)

    def start_page(self, page_url):
        driver = self.getDriver()
        #driver.get(f"{const.BASE_URL}/RestaurantSearch-g187791-oa{page_num*30}-a_date.2022__2D__06__2D__02-a_people.2-a_time.20%3A00%3A00-a_zur.2022__5F__06__5F__02-Rome_L.html#EATERY_LIST_CONTENTS")
        driver.get(page_url)
        sleep(self.small_sleep)
        try:
            driver.find_element(By.XPATH, "//button[text()='Accetto']").click()     #Accetta i cookie
            sleep(self.small_sleep)
        except Exception:
            pass
        next = driver.find_element(By.XPATH, "//div[@class='unified pagination js_pageLinks']/a[contains(text(),'Avanti')]")
        actionChains = ActionChains(driver)
        actionChains.move_to_element(next).perform()
        sleep(.5)
        next.click()
        sleep(2)
        return driver


    def getRestaurants(self, page_url):
        driver = self.getDriver()
        driver.get(page_url)
        sleep(3)
        actionChains = ActionChains(driver)
        container = driver.find_element(By.XPATH, "//div[@data-test-target='restaurants-list']")
        actionChains.move_to_element(container).perform()
        sleep(.15)
        for restaurant in container.find_elements(By.XPATH, ".//div[@class='cauvp Gi o']"):
            try:
                url_name = restaurant.find_element(By.XPATH, ".//a[@class='bHGqj Cj b']")
                url = url_name.get_attribute("href")
                name = url_name.text
                name = name[name.find('.')+1:].strip()
                total_reviews = restaurant.find_element(By.XPATH, ".//span[@class='NoCoR']").text # se non lo trova allora è un neo-ristorante
                try:
                    total_reviews = total_reviews[:total_reviews.find(' ')]
                    while '.' in total_reviews:
                        total_reviews = total_reviews.replace('.', '')
                    total_reviews = int(total_reviews)
                except ValueError as er:
                    print(f'[!]\t{er}')
                    total_reviews = total_reviews[:total_reviews.find(' ')]
                
                """if total_reviews < 50:
                    continue"""

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
                if not self.restaurant_cuisine_exist(url):
                    # get address by switching to next tab and then go back to main tab
                    restaurant_window = driver.current_window_handle
                    driver.execute_script("window.open('{}');".format(url))
                    driver.switch_to.window(driver.window_handles[-1])
                    sleep(.35)
                    try:
                        info_restaurant_box = driver.find_element(By.XPATH, "//div[@class='guXtP']")
                        for box in info_restaurant_box.find_elements(By.XPATH, ".//div/div[@class='dMshX b']"):
                            div_name = box.text.lower().strip()
                            i = info_restaurant_box.find_elements(By.XPATH, ".//div/div[@class='dMshX b']").index(box)
                            if div_name == 'cucine':
                                try:
                                    cuisines = info_restaurant_box.find_element(By.XPATH, f".//div[{i+1}]/div[@class='cfvAV']").text
                                    #print(f"{cuisines = }")
                                except Exception as e:
                                    print(e)
                                    cuisines = None
                                    #print(f"{cuisines = }")
                            elif div_name == 'diete speciali':
                                try:
                                    diets = info_restaurant_box.find_element(By.XPATH, f".//div[{i+1}]/div[@class='cfvAV']").text
                                    #print(f"{diets = }")
                                except Exception as e:
                                    print(e)
                                    diets = None
                                    #print(f"{diets = }")
                            else:
                                continue

                    except Exception as e:
                        print(e)
                        cuisines = None
                        diets = None

                    #try: 
                    #    restaurant_address = driver.find_element(By.XPATH, "//span[@class='brMTW']").text
                    #except Exception as e:
                    #    restaurant_address = None
                    
                    driver.close()
                    driver.switch_to.window(restaurant_window)

                    conn, cursor = db_connect()
                    cursor.execute("UPDATE restaurants SET cuisine = %s, diet = %s WHERE restaurant_url = %s",
                    (cuisines,
                    diets,
                    url))
                    conn.commit()
                    conn.close()

            except Exception as er:
                print(f'[!]\t{er}')
                continue
        
        driver.quit()
        return None


#    def getRestaurants(self, driver, page_num=0):
#        total_restaurants = int(driver.find_element(By.XPATH, ".//span[@class='ffdhf b']").text.strip())
#        pages = int(total_restaurants / 30)
#        actionChains = ActionChains(driver)
#        try:
#            for page in range(1+page_num,pages+1):
#                print(f"Getting page {page} / {pages}")
#                sleep(1)
#                container = driver.find_element(By.XPATH, "//div[@data-test-target='restaurants-list']")
#                actionChains.move_to_element(container).perform()
#                sleep(.15)
#                for restaurant in container.find_elements(By.XPATH, ".//div[@class='cauvp Gi o']"):
#                    try:
#                        url_name = restaurant.find_element(By.XPATH, ".//a[@class='bHGqj Cj b']")
#                        url = url_name.get_attribute("href")
#                        name = url_name.text
#                        name = name[name.find('.')+1:].strip()
#                        total_reviews = restaurant.find_element(By.XPATH, ".//span[@class='NoCoR']").text
#                        try:
#                            total_reviews = total_reviews[:total_reviews.find(' ')]
#                            while '.' in total_reviews:
#                                total_reviews = total_reviews.replace('.', '')
#                            total_reviews = int(total_reviews)
#                        except ValueError as er:
#                            print(f'[!]\t{er}')
#                            total_reviews = total_reviews[:total_reviews.find(' ')]
#                        
#                        if total_reviews < 200:
#                            continue
#
#                        rating = bs(restaurant.find_element(By.XPATH, ".//span[@class='bFlvo']").get_attribute("innerHTML"), 'html.parser').find('svg')['aria-label']
#                        rating = float(re.findall(r"[0-9]\,[0-9]", rating)[0].replace(',','.'))
#
#                        more_infos = restaurant.find_elements(By.XPATH, ".//span[@class='ceUbJ']")
#                        for info in more_infos:
#                            if "€" in info.text and '-' in info.text:
#                                price1,price2 = info.text.strip().split('-')
#                                price = (price1.count('€')+price2.count('€'))/2
#                            elif "€" in info.text:
#                                price = info.text.strip().count('€')
#
#                        # add to DB
#                        if not self.restaurant_exist(url):                            
#
#                            # get address by switching to next tab and then go back to main tab
#                            restaurant_window = driver.current_window_handle
#                            driver.execute_script("window.open('{}');".format(url))
#                            driver.switch_to.window(driver.window_handles[-1])
#                            sleep(.5)
#                            try: 
#                                restaurant_address = driver.find_element(By.XPATH, "//span[@class='brMTW']").text
#                            except Exception as e:
#                                restaurant_address = None
#
#                            conn, cursor = db_connect()
#                            cursor.execute("INSERT INTO restaurants VALUES (%s, %s, %s, %s, %s, %s)",
#                            (url,
#                            name,
#                            rating,
#                            total_reviews,
#                            price,
#                            restaurant_address))
#                            conn.commit()
#                            conn.close()
#
#                            driver.close()
#                            driver.switch_to.window(restaurant_window)
#
#                    except Exception as er:
#                        print(f'[!]\t{er}')
#                        continue
#                
#                next = driver.find_element(By.XPATH, "//div[@class='unified pagination js_pageLinks']/a[contains(text(),'Avanti')]")
#                actionChains.move_to_element(next).perform()
#                sleep(.5)
#                next.click()
#                sleep(1.5)
#        except KeyboardInterrupt:
#            driver.close()
#            print("[i]\texits gracefully 1")
#            sys.exit()
#
#        return None


    def restaurantUrls(self):
        conn, cursor = db_connect()
        cursor.execute("SELECT restaurant_url FROM restaurants")
        rows = cursor.fetchall()
        rows = [x[0] for x in rows]
        conn.commit()
        conn.close()
        return rows


    def getReviews(self, restaurant_url):
        driver = self.getDriver()
        driver.get(restaurant_url)
        start = time.perf_counter()
        try:
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accetto']"))).click()     #Accetta i cookie
            except Exception as e:
                pass

            #try: 
            #    restaurant_address = driver.find_element(By.XPATH, "//span[@class='brMTW']").text
            #except Exception as e:
            #    restaurant_address = None

            #conn, cursor = db_connect()
            #cursor.execute("UPDATE restaurants SET address=%s WHERE restaurant_url=%s", (restaurant_address,restaurant_url))
            #conn.commit()

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
            if pages > 1: 
                pages = 1 # max 200 per restaurant
            pages = pages+1

            #if pages < 11:
            #    driver.quit()
            #    return
            for page in range(1,pages+1):
                print(f"[i] Getting page {page} / {pages}")
                try:
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='taLnk ulBlueLinks']"))).click()
                except Exception as e:
                    pass
                
                try:
                    container = driver.find_elements(By.XPATH, "//div[@class='review-container']")
                    actions = ActionChains(driver)
                    actions.move_to_element(container[0]).perform()
                except Exception as e:
                    pass
                
                skipped = 0
                for i in range(0, len(container)):
                    # if exists, skip
                    review_url = container[i].find_element(By.XPATH, ".//a[@class='title ']").get_attribute("href")
                    if self.review_exist(review_url):
                        skipped += 1
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
                        #stop = time.perf_counter()
                        #print(f"[i] page n°{page} took {stop - start:0.4f} seconds")
                        continue
                    

                    actions.move_to_element(container[i].find_element(By.XPATH, ".//span[@class='noQuotes']")).perform()
                    
                    avatar = WebDriverWait(container[i], 120).until(EC.element_to_be_clickable((By.XPATH, ".//div[contains(@class, 'ui_avatar resp')]")))
                    avatar.click()
                    sleep(0.5)
                    
                    reviewer_box = WebDriverWait(container[i], 120).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'memberOverlayRedesign g10n')]/a")))
                    
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
                        conn, cursor = db_connect()
                        cursor.execute("INSERT INTO reviews VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
                        conn.commit()
                        conn.close()

                    if not self.user_exist(user=reviewer_name):
                        conn, cursor = db_connect()
                        cursor.execute("INSERT INTO reviewers VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
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

                    WebDriverWait(driver, 120).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@class='ui_overlay ui_popover arrow_left ']/div[@class='ui_close_x']"))
                        ).click()

                stop = time.perf_counter()
                print(f"[i] page n°{page} took {stop - start:0.4f} seconds;\t reviews skipped = {skipped}")
                
                try:
                    next = driver.find_element(By.XPATH, "//div[@class='unified ui_pagination ']/a[contains(text(),'Avanti')]")
                    actionChains = ActionChains(driver)
                    actionChains.move_to_element(next).perform()
                    sleep(.75)
                    next.click()
                except Exception as e:
                    #tb = sys.exc_info()[2]
                    #print(e.with_traceback(tb))
                    break
                

            try:
                conn.close()
            except UnboundLocalError:
                pass
        except Exception as e:
            print("[i]\texits gracefully")
            #sys.exit()
        driver.quit()
        return

    @staticmethod
    def getRestaurantsTrheshold(threshold):
        conn, cursor = db_connect()
        cursor.execute("SELECT `restaurant_url` FROM (SELECT restaurants.restaurant_url, COUNT(*) AS n_review FROM restaurants INNER JOIN reviews ON restaurants.restaurant_url = reviews.restaurant_url GROUP BY restaurants.restaurant_url) as a WHERE `n_review` < %s;", (threshold,))
        conn.commit()
        result = cursor.fetchall()
        rows = [x[0] for x in result]
        conn.close()
        return rows, len(rows)
    
    @staticmethod
    def not_reviewed_restaurant():
        conn, cursor = db_connect()
        cursor.execute("SELECT restaurants.restaurant_url FROM restaurants WHERE restaurants.restaurant_url NOT IN (SELECT reviews.restaurant_url FROM reviews)")
        conn.commit()
        result = cursor.fetchall()
        rows = [x[0] for x in result]
        conn.close()
        return rows


    @staticmethod
    def get_all_reviews():
        conn, cursor = db_connect()
        cursor.execute("SELECT review_text FROM reviews")
        res = cursor.fetchall()
        conn.close()
        res = [x[0].decode("utf-8") for x in res]
        print("[SQL] Sending result...")
        return res


    @staticmethod
    def tokenize(reviews):
        final_reviews = []

        italian_stopwords = stopwords.words("italian")
        tokenizer = RegexpTokenizer(r'\w+')
        for review in reviews:
            lower_review = review.lower()
            filtered_sentence = tokenizer.tokenize(lower_review)
            filtered_sentence = ' '.join(filtered_sentence)
            word_tokens = word_tokenize(filtered_sentence)
            filtered_sentence = [w for w in word_tokens if not w in italian_stopwords]
            cleaned_review = ' '.join(filtered_sentence)
            final_reviews.append(cleaned_review)
        print("[NLTK] Finished preprocessing...")
        return final_reviews

    @staticmethod
    def wordcloud(reviews, max_words: int, border: bool, img_path, subsample: str = None):
        subsamples = {"small": 1, "medium": 2, "large": 3}

        d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()

        try:
            img_color = np.array(Image.open(os.path.join(d, f"{img_path}.jpg")))
        except FileNotFoundError:
            img_color = np.array(Image.open(os.path.join(d, f"{img_path}.png")))

        if subsample:
            img_color = img_color[::subsamples.get(subsample), ::subsamples.get(subsample)]

        img_mask = img_color.copy()
        img_mask[img_mask.sum(axis=2) == 0] = 255
        edges = np.mean([gaussian_gradient_magnitude(img_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
        img_mask[edges > .08] = 255
        if border:
            wc = wordcloud = WordCloud(
                mask = img_mask,
                background_color = 'black',
                max_words = max_words,
                max_font_size = 500,
                random_state = 42,
                contour_width=1, 
                contour_color='black',
                relative_scaling=0
                ).generate(' '.join([i for i in reviews]))
        else:
            wc = wordcloud = WordCloud(
                mask = img_mask,
                background_color = 'black',
                max_words = max_words,
                max_font_size = 40,
                random_state = 42,
                relative_scaling=0
                ).generate(' '.join([i for i in reviews]))
        image_colors = ImageColorGenerator(img_color)
        wc.recolor(color_func=image_colors)
        plt.imshow(wordcloud, interpolation="bilinear") # image show
        plt.axis('off') # to off the axis of x and y
        plt.savefig(f'wc_{img_path}.png')
        plt.show()

if __name__ == "__main__":
    from collections import Counter
    import pandas as pd
    import plotly.express as px
    Bot = PyTripAdvisor()
    Bot.clear()
    final_count_dict = {}
    recensioni = Bot.get_all_reviews()
    recensioni_pulite = Bot.tokenize(recensioni)
    for recensione in recensioni_pulite:
        recensione_lista_parole = recensione.split(" ")
        recensione_dict_count = Counter(recensione_lista_parole)
        final_count_dict = mergeDictionary(final_count_dict, recensione_dict_count)

    d = {k: v for k, v in sorted(final_count_dict.items(), key=lambda item: item[1], reverse=True)}
    df = pd.DataFrame({x:[y] for x,y in d.items()}).T
    df = df.iloc[:20]
    df.plot(kind='bar')
    plt.show()
    #fig = px.histogram(df, x="")
    #fig.show()

    

    #Bot.user_exist('pippo')
    #driver = Bot.getDriver()
    #try:
    #Bot.search(driver)
    #Bot.start_page(driver,page_num=89)
    #Bot.getRestaurants(driver,page_num=0)
    #urls = Bot.restaurantUrls()
    #urls = Bot.not_reviewed_restaurant() #7404

    # 7236 13:52
    # 7000 14:12
    # 6687 14:52
    # 6634 15:09
    # 6454 15:30
    # 5061 19:07
    # 4143 21:30
    # 3411 00:30


    # SELECT COUNT(*) FROM (SELECT restaurants.restaurant_url FROM restaurants WHERE restaurants.restaurant_url NOT IN (SELECT reviews.restaurant_url FROM reviews)) as B

    #with ProcessPoolExecutor(max_workers=12) as executor:
    #    result = [executor.map(Bot.getReviews, urls)]

    #Bot.getReviews(driver, urls)
    #review_text = Bot.tokenize("Ho pranzato presso il Leggiadria Restaurant in compagnia di 5 amici.")
    #Bot.wordcloud(review_text)
    #Bot.wordcloud(Bot.tokenize(Bot.get_all_reviews()))