import os
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PC_project.settings')
import django

django.setup()

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from splinter import Browser
from selenium import webdriver
from crawler.models import UserInfo


def dominosForm():
    # ścieżka do chromedrivera
    executable_path = {"executable_path": r"/Users/michaljanusz/workspace/chromedriver/chromedriver"}

    # opcje przeglądarki
    options = webdriver.ChromeOptions()

    # opcja włączenia maksymalizacji
    options.add_argument("--start-maximized")

    # opcja wylaczenia powiadomien
    options.add_argument("--disable-notifications")

    # tworzę obiekt przeglądarki splinter
    browser = Browser('chrome', **executable_path, headless=False, options=options)

    browser.driver.maximize_window()

    # wejście na strone dominos
    browser.visit('https://www.dominospizza.pl/pl')
    # time.sleep(1)

    rabat_prompt = browser.find_by_xpath('//*[@id="jsNewsletterLayer"]/span')
    rabat_prompt.click()

    zamow_button = browser.find_by_xpath('//*[@id="jsIndexNav1"]/a')
    zamow_button.click()

    # pobieram dane z modelu
    user_info = UserInfo.objects.get(user_id=3)

    city = user_info.city
    street = user_info.street
    house_nr = user_info.house_nr
    flat_nr = user_info.flat_nr
    if flat_nr is None:
        flat_nr = ''

    form_values = {'city': city, 'street': street, 'housenumber': house_nr, 'flatnumber': flat_nr}

    browser.fill_form(form_values, 'jsDeliveryForm')
    browser.find_by_id('jsDeliveryFormBtn').click()

    start_order = browser.find_by_xpath('//*[@id="jsDeliveryFormSubmit"]')
    start_order.click()

    pizza_button = browser.find_by_xpath('//*[@id="wrapper"]/div[3]/div/div/div/div[1]/div/nav/ul/li[2]/a')
    pizza_button.click()

    cookie_button = browser.find_by_xpath('//*[@id="hide-cookie-info"]')
    cookie_button.click()

    pepperoni_button = browser.find_by_xpath(
        '//*[@id="wrapper"]/div[3]/div/div/div/div[1]/div/article/section[5]/div/div/div[3]/span')
    pepperoni_button.click()

    WebDriverWait(browser.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="jsCreatorForm"]/div[1]/section[2]/button'))).click()

    order_button = browser.find_by_xpath(
        '//*[@id="wrapper"]/div[3]/div/div/div/div[3]/aside/section[1]/div[2]/div[2]/span')
    order_button.click()

    continue_button = browser.find_by_xpath('//*[@id="jsRecommendedLayer"]/div/div[2]/a')
    continue_button.click()

    order_info_button = browser.find_by_xpath('//*[@id="jsOrderSummaryC"]/div/a[2]')
    order_info_button.click()
