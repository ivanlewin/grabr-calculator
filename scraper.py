from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep


def load_driver():

    driver = webdriver.Firefox(executable_path="../../geckodriver.exe")

    return driver


def wait_for_element(driver, selector, count=0):

    while count < 15:

        try:
            element = driver.find_element_by_css_selector(selector)
            return element

        except NoSuchElementException:
            sleep(1)
            wait_for_element(driver, selector, count+1)

    else:
        raise NoSuchElementException("Waited 15 seconds for element to load but couldn't find it.")


def load_grabr(driver, email, password):

    def sign_in(driver):

        email_input = wait_for_element(driver, "input[type='email']")
        password_input = driver.find_element_by_css_selector("input[type='password']")

        email_input.send_keys(email)
        password_input.send_keys(password)

        sleep(3)

        log_in_button = driver.find_element_by_css_selector("button[data-persistent-id='click.sign-in-with-email']")
        log_in_button.click()

        return driver

    driver.get("https://grabr.io/login")
    sleep(3)

    if driver.current_url.endswith("login"):  # If not redirected to main page (e.g.: a profile with a stored session)

        with_email = wait_for_element(driver, "button.mt5")
        with_email.click()

        logged_in = sign_in(driver)

        # Search for an error banner.
        try:
            logged_in.find_element_by_css_selector("._13._14")
            raise Exception("Log in error, close the script and try again in a few minutes.")

        except NoSuchElementException:
            return logged_in


def fill_in_price(driver, price):

    price_input = wait_for_element(driver, "input[type='number']")
    price_input.clear()
    price_input.send_keys(str(price))

    next_button = driver.find_element_by_css_selector(".p5 div[role='button']")
    # to avoid ElementClickInterceptedException
    driver.execute_script("document.documentElement.scrollTop = 0")
    next_button.click()

    return driver


def fill_delivery_city(driver, city):

    city_input = wait_for_element(driver, "input[placeholder='City']")
    city_input.clear()
    city_input.send_keys(city)

    city_button = wait_for_element(driver, ".pt8 .py1")
    city_button.click()

    next_button = driver.find_element_by_css_selector(".LG_gc4 button")
    next_button.click()

    return driver


def price_breakdown(driver):

    price_table = wait_for_element(driver, ".py4")

    price_items = price_table.find_elements_by_css_selector(".pr3")

    for item in price_items:

        name = item.text
        row = item.find_element_by_xpath("parent::div/parent::div")
        value = int(''.join(i for i in row.text if i.isdigit()))

        print(f"{name} : {value}")


    order_total = price_table.find_element_by_xpath("following-sibling::div")
    usd_price = int(''.join(i for i in order_total.text if i.isdigit()))

    total_in_ars = order_total.find_element_by_xpath("following-sibling::div")
    ars_price = int(''.join(i for i in total_in_ars.text if i.isdigit()))

    print(usd_price, ars_price)


def main():

    with open("credentials.txt", "r") as f:
        email, password= f.read().splitlines()

    driver = load_driver()

    driver = load_grabr(driver, email, password)

    driver.get(f"https://grabr.io/en/grabs/new?url=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-iphone%2Fiphone-11-pro")

    fill_in_price(driver, price=100)

    fill_delivery_city(driver, city="Buenos Aires")

    price_breakdown(driver)

    driver.quit()


if __name__ == '__main__':
    main()
