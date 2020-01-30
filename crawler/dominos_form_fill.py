import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PC_project.settings')
import django

django.setup()

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from splinter import Browser
from selenium import webdriver
from django.contrib.auth.models import User


def first_step_ordering(user, additional, payment):
    result, browser = dominos_order_process(user, additional, payment)

    return result


def dominos_order_process(user, additional, payment):
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

    # wyłączam prompt o rabacie
    rabat_prompt = browser.find_by_xpath('//*[@id="jsNewsletterLayer"]/span')
    rabat_prompt.click()

    # otwieram zakładkę zamówienia
    zamow_button = browser.find_by_xpath('//*[@id="jsIndexNav1"]/a')
    zamow_button.click()

    city = user.userinfo.city
    street = user.userinfo.street
    house_nr = user.userinfo.house_nr
    flat_nr = user.userinfo.flat_nr
    phone = user.userinfo.phone
    if flat_nr is None:
        flat_nr = ''

    # dane z modelu przygotowane do wypełnienia formularza
    form_values = {'city': city, 'street': street, 'housenumber': house_nr, 'flatnumber': flat_nr}

    # wypełniam formularz danymi i potwierdzam
    browser.fill_form(form_values, 'jsDeliveryForm')
    browser.find_by_id('jsDeliveryFormBtn').click()

    # rozpoczynam zamówienie
    start_order = browser.find_by_xpath('//*[@id="jsDeliveryFormSubmit"]')
    start_order.click()

    # przechodzę do strony z listą pizz
    pizza_button = browser.find_by_xpath('//*[@id="wrapper"]/div[3]/div/div/div/div[1]/div/nav/ul/li[2]/a')
    pizza_button.click()

    # wyłączam komunikat o plikach cookie
    cookie_button = browser.find_by_xpath('//*[@id="hide-cookie-info"]')
    cookie_button.click()

    # naciskam przycisk od pizzy pepperoni
    pepperoni_button = browser.find_by_xpath(
        '//*[@id="wrapper"]/div[3]/div/div/div/div[1]/div/article/section[5]/div/div/div[3]/span')
    pepperoni_button.click()

    # naciskam przycisk dodania do koszyka
    WebDriverWait(browser.driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="jsCreatorForm"]/div[1]/section[2]/button'))).click()

    # naciskam przycisk potwierdzenia zamówienia
    order_button = browser.find_by_xpath(
        '//*[@id="wrapper"]/div[3]/div/div/div/div[3]/aside/section[1]/div[2]/div[2]/span')
    order_button.click()

    # naciskam przycisk pominięcia proponowanych dodatków
    continue_button = browser.find_by_xpath('//*[@id="jsRecommendedLayer"]/div/div[2]/a')
    continue_button.click()

    # pobieram i formatuję nazwę zamówionego produktu
    raw_items = browser.find_by_xpath('//*[@id="jsOrderSummaryC"]/section/section[1]/dl[1]/dt/div').html
    order_items = raw_items.replace('\t', '').replace('\n', '')

    # pobieram i formatuję cene zamówienia
    raw_price = browser.find_by_xpath('//*[@id="jsOrderSummaryC"]/section/section[2]/div[2]/dl/dd').html
    order_price = raw_price.replace('\t', '').replace('\n', '').replace('   ', '')

    # naciskam przycisk przejścia do zakładki 3 z formularzem
    order_info_button = browser.find_by_xpath('//*[@id="jsOrderSummaryC"]/div/a[2]')
    order_info_button.click()

    last_form_values = {'firstname': user.first_name, 'lastname': user.last_name, 'phone': phone,
                        'deliveryinstruction': additional, 'email': user.email, 'paymenttypeid': payment}
    browser.fill_form(last_form_values, 'jsAddressDetailsForm')

    result = {'city': city, 'street': street, 'house_nr': house_nr, 'flat_nr': flat_nr, 'order_items': order_items,
              'order_price': order_price, 'firstname': user.first_name, 'lastname': user.last_name, 'phone': phone,
              'deliveryinstruction': additional, 'email': user.email}
    return result, browser


if __name__ == "__main__":
    usr = User.objects.get(pk=3)

    info = 'Biurowiec, proszę dzwonić na podany numer telefonu'

    print(dominos_order_process(user=usr, additional=info, payment=1))
