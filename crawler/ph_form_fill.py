import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PC_project.settings')
import django

django.setup()

from splinter import Browser
from selenium import webdriver
from crawler.models import UserInfo

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def phForm():
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

    # wejście na strone PH
    browser.visit('https://pizzahut.pl')

    # znalezienie i kliknięcie przycisku od cookies
    cookies = browser.find_by_text(' OK, ROZUMIEM ')
    print(type(cookies))
    cookies.click()

    # znalezienie przycisku od zamawiania
    localize = browser.find_by_css('.ph-btn-enter-address-manually').first
    localize.click()

    # pobieram dane z modelu
    user_info = UserInfo.objects.get(user_id=3)

    city = user_info.city
    street = user_info.street
    house_nr = user_info.house_nr
    flat_nr = user_info.flat_nr
    if flat_nr is None:
        flat_nr = ''

    form_values = {'city': city, 'street': street, 'streetNo': house_nr, 'flatNo': flat_nr}

    browser.fill_form(form_values, 'deliveryForm')

    browser.find_by_id('submitPhOrder').click()

    # submitPhOrder
    browser.visit('https://pizzahut.pl/products#category/pizza')

    # WebDriverWait(browser.driver, 20).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="ph-add-to-basket-61500242"]/div[1]'))).click()
    #
    # input('wez nacisnij cos')

# TO GÓWNO NIE DZIAŁA ://///#
