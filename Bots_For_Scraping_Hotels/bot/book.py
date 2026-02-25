from types import TracebackType
from typing import Type
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import bot.values as val
import time
import os

class Book(webdriver.Chrome):
    # Initializes the Book() class and instantiates the inherited class
    def __init__(self, teardown=False):
        self.teardown = teardown
        self.instance = val.Values()
        self.ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        super(Book, self).__init__()

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None):
        if self.teardown:
            self.quit()

    # Lands on the base URL
    def land_first_page(self):
        self.get(self.instance.base_url)
        
    def remove_cookie_mssg(self):
        q = '/html/body/div[1]/div[2]/footer/div[3]/div[2]/div[1]/h2/span'
        time.sleep(10)
        try:
            self.find_element("xpath", q).click()
        except:
            print("Exiting...")

    def remove_popup(self):
        self.implicitly_wait(10)
        try:
            self.find_element("xpath", '/html/body/section[2]/dialog/div/button').click()
        except:
            print("No popup mssg. Proceeding....")

    # Navigates to the country specific website
    def select_website(self):
        c = self.instance.country
        cq = f'//select[@name="country"]'
        dropdown = Select(self.find_element("xpath", cq))
        dropdown.select_by_visible_text(c)
        self.remove_cookie_mssg()

    # Selects language and currency
    def select_lan_cur(self):
        l = self.instance.lan
        c = self.instance.cur
        self.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div/header/nav/ul/li[2]/button').click()
        lang_dropdown = Select(self.find_element("xpath", '//select[@id="language-select"]'))
        lang_dropdown.select_by_visible_text(l)
        cur_dropdown = Select(self.find_element("xpath", '/html/body/section[1]/dialog/div/div/form/div[2]/span/select'))
        cur_dropdown.select_by_value(c)
        self.find_element("xpath", '/html/body/section[1]/dialog/div/div/form/div[3]/button').click()
        #time.sleep(4)
        self.select_destination()
    
    def select_destination(self):
        search_element = WebDriverWait(self, 20, ignored_exceptions=self.ignored_exceptions).until(EC.visibility_of_element_located((By.ID, 'input-auto-complete')))
        search_element.clear()
        search_element.send_keys(self.instance.destination)
        WebDriverWait(self, 20, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="suggestion-list"]/ul/li[1]'))).click()
        self.check_in_and_out()

    def check_in_and_out(self):
        while self.instance.check_in > 0:
            WebDriverWait(self, 20, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/div/div/div[2]/button[2]'))).click()
            self.instance.check_in -= 1

        WebDriverWait(self, 20, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.XPATH, f'//button[@data-testid="valid-calendar-day-{self.instance.cid}"]'))).click()

        while self.instance.check_out > 0:
            WebDriverWait(self, 20, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/div/div/div[2]/button[2]'))).click()
            self.instance.check_out -= 1

        WebDriverWait(self, 20, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.XPATH, f'//button[@data-testid="valid-calendar-day-{self.instance.cod}"]'))).click()

        self.select_rooms()

    def select_rooms(self):
        WebDriverWait(self, 20, ignored_exceptions=self.ignored_exceptions).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/section/div/div/div[1]/div[1]/div/button[1]'))).click()
        for _ in range(2, self.instance.adult_num+1):
            self.find_element("xpath", '//*[@id="__next"]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/section/div/div/div[1]/div[1]/div/button[2]').click()

        for _ in range(1, self.instance.child_num+1):
            self.find_element("xpath", '//*[@id="__next"]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/section/div/div/div[1]/div[2]/div/button[2]').click()


        for _ in range(1, self.instance.reqd_room_num+1):
            self.find_element("xpath", '//*[@id="__next"]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/section/div/div/div[1]/div[3]/div/button[2]').click()

        for num in range(1, self.instance.children+1):
            child_ele = Select(WebDriverWait(self, 20, ignored_exceptions=self.ignored_exceptions).until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[1]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/section/div/div/div[2]/fieldset/ul/li[{num}]/div/div/div/span/select'))))
            child_ele = Select(self.find_element("xpath", f'/html/body/div[1]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/section/div/div/div[2]/fieldset/ul/li[{num}]/div/div/div/span/select'))
            child_ele.select_by_value(self.instance.children_age_list[num-1])

        if self.instance.is_pet_friendly:
            self.find_element("xpath", '/html/body/div[1]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/section/div/div/div[3]/div/label/input').click()
        
        self.find_element("xpath", '/html/body/div[1]/div[1]/div[2]/section[1]/div[2]/div[4]/div/div[2]/div/section/footer/button[2]').click()
        

    # Lands on the results page, scrapes raw html and stores them one by one inside a directory called data
    def get_items(self):
        time.sleep(10)
        
        eles = self.find_elements("xpath", '//li[@data-testid="accommodation-list-element"]')
        
        if not os.path.exists('bot/raw_data'):
            os.makedirs('bot/raw_data')
        file_num = 1
        track = dict()
        for ele in eles:
            time.sleep(5)
            button = ele.find_element(By.CSS_SELECTOR, ".DealButton_nuxClickoutBtn__OAJXD")
            url_ = ""
            try:
                button.click()
                window_handles = self.window_handles
                self.switch_to.window(window_handles[-1])
                url_ = self.current_url
                self.close()
                self.switch_to.window(window_handles[0])
            except Exception as e:
                url_ = "NA"
                print(e)
            track[file_num] = []
            track[file_num].append(url_)

            h = ele.get_attribute("outerHTML").encode('utf8').decode('ascii', 'ignore')
            with open(f"bot/raw_data/hotel_{file_num}.html", "w") as f:
                f.write(h)
                track[file_num].append(f"bot/raw_data/hotel_{file_num}.html")
                file_num += 1

        return track
                

        
        
    
        
       
        