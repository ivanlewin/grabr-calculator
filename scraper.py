# import os
# from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
# from random import randint


def load_driver():

    driver = webdriver.Firefox(executable_path="../../geckodriver.exe")

    return driver


def wait_for_element(driver, selector):

    try:
        driver.find_element_by_css_selector(selector)

    except NoSuchElementException:
        sleep(1)
        wait_for_element(driver, selector)

    return


def load_grabr(driver, email, password):

    def with_email(driver):

        login_with_email = driver.find_element_by_css_selector("button.mt5")
        login_with_email.click()

        return driver

    def sign_in(driver):

        email_input = driver.find_element_by_css_selector("input[type='email']")
        password_input = driver.find_element_by_css_selector("input[type='password']")

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)

        log_in_button = driver.find_element_by_css_selector("button[data-persistent-id='click.sign-in-with-email']")
        log_in_button.click()

        return driver

    driver.get("https://grabr.io/login")
    sleep(3)

    if driver.current_url.endswith("login"):  # If not redirected to main page (e.g.: a profile with a stored session)

        wait_for_element(driver, "button.mt5")
        email_screen = with_email(driver)

        wait_for_element(email_screen, ".input")
        sign_in(email_screen)

        sleep(3)

        # Search for an error banner.
        try:
            driver.find_element_by_css_selector("._13._14")
            print("Log in error, close the script and try again in a few minutes.")
            raise

        except NoSuchElementException:
            return driver


def fill_in_price(driver, price):

    price_input = driver.find_element_by_css_selector("input[type='number']")
    price_input.clear()
    price_input.send_keys(str(price))

    next_button = driver.find_element_by_css_selector(".p5 div[role='button']")
    # to avoid ElementClickInterceptedException
    driver.execute_script("document.documentElement.scrollTop = 0")
    next_button.click()

    return driver


def fill_delivery_city(driver, city="Buenos Aires"):

    def check_city_registered():

        city_input.send_keys(Keys.ENTER)
        city_and_date_details = driver.find_element_by_css_selector(".py5:nth-child(2)")
        does_city_appear = driver.execute_script("arguments[0].children.length;", city_and_date_details)

        print(does_city_appear)

        while does_city_appear != 3:
            sleep(1)
            check_city_registered()

        next_button = driver.find_element_by_css_selector(".LG_gc4 button")
        next_button.click()

    try:
        city_input = driver.find_element_by_css_selector("input[placeholder='City']")
        city_input.clear()
        city_input.send_keys(city)

    except NoSuchElementException:
        sleep(1)
        fill_delivery_city(driver)

    finally:
        check_city_registered()


def read_prices(driver):

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
        read_prices(driver)


def main():

    with open("credentials.txt", "r") as f:
        email, password= f.readlines()

    driver = load_driver()
    load_grabr(driver, email, password)

    product_details_page = driver.get(f"https://grabr.io/en/grabs/new?url=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-iphone%2Fiphone-11-pro")

    wait_for_element(product_details_page, ".SM_pb5")
    fill_in_price(product_details_page)

    fill_delivery_city(driver)
    read_prices(driver)


if __name__ == '__main__':
    main()
