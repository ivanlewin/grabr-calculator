import os
import pandas as pd
from datetime import datetime
from re import match
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep


def load_driver():

    global driver

    firefox_profile = None
    driver = webdriver.Firefox(firefox_profile, executable_path="../../geckodriver.exe")

    return driver


def load_grabr(email, password):

    if not (email and password):
        raise BaseException

    login_page = "https://grabr.io/login"
    driver.get(login_page)
    sleep(2)

    try:

        login_with_email = driver.find_element_by_css_selector("button.mt5")
        login_with_email.click()
        sleep(3)

        email_input = driver.find_element_by_css_selector("input[type='email']")
        password_input = driver.find_element_by_css_selector("input[type='password']")

        email_input.send_keys(email)
        password_input.send_keys(password)
        log_in_button = driver.find_element_by_css_selector("button[data-persistent-id='click.sign-in-with-email']")
        log_in_button.click()

    except NoSuchElementException:
        pass


def fill_product_details(price=100):

    try:

        price_input = driver.find_element_by_css_selector("input[type='number']")
        price_input.clear()
        price_input.send_keys(str(price))

        next_button = driver.find_element_by_css_selector(".p5 div[role='button']")
        # to avoid ElementClickInterceptedException
        driver.execute_script("document.documentElement.scrollTop = 0")
        next_button.click()

        return

    except NoSuchElementException:
        sleep(1)
        fill_product_details()


def fill_delivery_city(city="Buenos Aires"):

    try:
        deliver_to = driver.find_element_by_css_selector("input[placeholder='City']")
        deliver_to.clear()
        deliver_to.send_keys(city)

    except NoSuchElementException:
        sleep(1)
        fill_delivery_city()


def press_city_button():

    try:
        city_button = driver.find_element_by_css_selector(".pt8 > div:nth-child(2) > label:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div")
        city_button.click()

        next_button = driver.find_element_by_css_selector(".LG_gc4 button")
        next_button.click()

    except NoSuchElementException:
        sleep(1)
        press_city_button()


def read_prices():

    try:
        price_table = driver.find_element_by_css_selector(".py4")
        order_total = price_table.find_element_by_xpath("following-sibling::div")
        usd_price = ''.join(i for i in order_total.text if i.isdigit())
        total_in_ars = order_total.find_element_by_xpath("following-sibling::div")
        ars_price = ''.join(i for i in total_in_ars.text if i.isdigit())
        payment_time = driver.find_element_by_css_selector(
            ".d-n.SM_pt5>div:nth-of-type(1)>div.mt5")

    except NoSuchElementException:
        sleep(1)
        read_prices()


def main():

    email = ""
    password = ""

    load_driver()
    load_grabr(email, password)
    driver.get(r"https://grabr.io/en/grabs/new?url=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-iphone%2Fiphone-11-pro")
    fill_product_details()
    fill_delivery_city()
    press_city_button()
    read_prices()


if __name__ == '__main__':
    main()
