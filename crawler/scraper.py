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
    browser = Browser('chrome', **executable_path, headless=False, options=options)
    return browser


def price_to_float(raw_price):
    str_price = raw_price[:5].replace(',', '.')
    price = float(str_price)
    return price
# Pepperoni = 1
# Hawajska = 2
# Margherita = 3
# Szynka Pieczarki = 4
# 4 sery = 5


def ph_scraper(pizza):
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

    with turn_on_browser() as browser:
        url = 'https://pizzahut.pl/menu/preview/delivery#category/pizza'
        browser.visit(url)

        # SZUKAM NAZWY PIZZY
        ph_name = browser.find_link_by_partial_text(search).find_by_tag('h5')

        # FORMATUJE NAZWE
        name = ph_name.html[0:16].split('\n')[0]

        # SZUKAM CENY
        raw_price = browser.find_link_by_partial_text(search).find_by_tag('p').first.html

        # FORMATUJE CENE
        price = price_to_float(raw_price)

        # PRZEMYSLEC JESZCZE W JAKI SPOSOB ZWRACAM DANE
        result = {'name': name.capitalize(), 'price': price}
    return result


# TESTY
# print(ph_scraper(1))
# print(ph_scraper(2))
# print(ph_scraper(3))
# print(ph_scraper(4))
# print(ph_scraper(5))

def dominos_scraper(pizza):
    if pizza == 1:
        search = 4  # Pepperoni
    elif pizza == 2:
        search = 5  # Hawajska
    elif pizza == 3:
        search = 7  # Margherita
    elif pizza == 4:
        search = 6  # szynka pieczarki
    elif pizza == 5:
        return {'name': 'Nie istnieje', 'price': 'troche kiepsko'}
    else:
        return None

    with turn_on_browser() as browser:
        url = 'https://www.dominospizza.pl/pl/oferta/menu/sl/pizza'
        browser.visit(url)

        # ZNAJDUJE DIVA W KTORYM SA INFORMACJE O PIZZY
        pizza_div = browser.find_by_xpath(f'//*[@id="promo-tab-pizza"]/div/div[{search}]')

        # ZNAJDUJE TAG H4 W KTORYM JEST NAZWA PICCY
        pizza_h4 = pizza_div.find_by_tag('h4').html

        # FORMATUJE NAZWE
        raw_name = pizza_h4.split('<')[0]
        name = raw_name.replace('\n', '').replace(' ', '')

        # SZUKAM I FORMATUJE CENE
        pizza_price = pizza_div.find_by_css('.offer-item-price')[1].html
        raw_price = pizza_price.replace(' ', '').replace('\n', '')
        price = price_to_float(raw_price)

        result = {'name': name, 'price': price}
        return result


# print(dominos_scraper(1))
