import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PC_project.settings')
import django

django.setup()

from splinter import Browser
from selenium import webdriver

# ścieżka do chromedrivera
executable_path = {"executable_path": r"/Users/michaljanusz/workspace/chromedriver/chromedriver"}

# opcje przeglądarki
options = webdriver.ChromeOptions()

# opcja włączenia maksymalizacji
options.add_argument("--start-maximized")

# opcja wylaczenia powiadomien
options.add_argument("--disable-notifications")


# tworzę obiekt przeglądarki splinter
def turn_on_browser():
    browser = Browser('chrome', **executable_path, headless=True, options=options)
    return browser

# Pepperoni = 1
# Hawajska = 2
# Margherita = 3
# Szynka Pieczarki = 4
# 4 sery = 5


def ph_scraper(pizza):
    with turn_on_browser() as browser:
        url = 'https://pizzahut.pl/menu/preview/delivery#category/pizza'
        browser.visit(url)

        if pizza == 1:
            search = 'PEPPERONI'
        elif pizza == 2:
            search = 'HAWAJSKA'
        elif pizza == 3:
            search = 'MARGHERITA'
        elif pizza == 4:
            search = 'CLASSICA'
        elif pizza == 5:
            search = 'QUATTRO FORMAGGI'
        else:
            return None

        # SZUKAM NAZWY PIZZY
        test = browser.find_link_by_partial_text(search).find_by_tag('h5')

        # FORMATUJE NAZWE
        name = test.html[0:16].split('\n')[0]

        # SZUKAM CENY
        raw_price = browser.find_link_by_partial_text(search).find_by_tag('p').first.html

        # FORMATUJE CENE
        str_price = raw_price[:5].replace(',', '.')
        price = float(str_price)

        # PRZEMYSLEC JESZCZE W JAKI SPOSOB ZWRACAM DANE
        result = {'name': name.capitalize(), 'price': price}
    return result


# TESTY
# print(ph_scraper(1))
# print(ph_scraper(2))
# print(ph_scraper(3))
# print(ph_scraper(4))
# print(ph_scraper(5))
