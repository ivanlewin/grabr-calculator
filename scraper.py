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
	driver = webdriver.Firefox(
		firefox_profile, executable_path="../../geckodriver.exe")

	return driver


def load_grabr(email="", password=""):

	login_page = "https://grabr.io/login"
	driver.get(login_page)
	sleep(2)

	try:

		login_with_email = driver.find_element_by_css_selector("button.mt5")
		login_with_email.click()
		sleep(3)

		email_input = driver.find_element_by_css_selector(
			"input[type='email']")
		password_input = driver.find_element_by_css_selector(
			"input[type='password']")

		email_input.send_keys(email)
		password_input.send_keys(password)
		log_in_button = driver.find_element_by_css_selector(
			"button[data-persistent-id='click.sign-in-with-email']")
		log_in_button.click()

	except NoSuchElementException:
		pass


def create_order():

	def fill_product_details():

		try:

			price_input = driver.find_element_by_css_selector("input[type='number']")
			price_input.send_keys("100")

			next_button = driver.find_element_by_css_selector(".p5 div[role='button']")
			driver.execute_script("document.documentElement.scrollTop = 0")
			next_button.click()

			return
			
		except NoSuchElementException:
			fill_product_details()

	def fill_delivery_city():

		try:
			deliver_to = driver.find_element_by_css_selector("input[placeholder='City']")
			deliver_to.clear()
			deliver_to.send_keys("Buenos Aires")
			sleep(3)
			buenos_aires_button = driver.find_element_by_css_selector(".pt8 > div:nth-child(2) > label:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div")
			buenos_aires_button.click()
			next_button = driver.find_element_by_css_selector(".LG_gc4 button")
			next_button.click()

		except NoSuchElementException:
			fill_delivery_city()


	driver.get(r"https://grabr.io/en/grabs/new?url=https%3A%2F%2Fwww.apple.com%2Fshop%2Fbuy-iphone%2Fiphone-11-pro")

	fill_product_details()

	fill_delivery_city()

	#On Your order summary
	price_table = driver.find_element_by_css_selector(".py4")
	order_total = price_table.find_element_by_xpath("following-sibling::div")
	usd_price = ''.join(i for i in order_total.text if i.isdigit())
	total_in_ars = order_total.find_element_by_xpath("following-sibling::div")
	ars_price = ''.join(i for i in total_in_ars.text if i.isdigit())
	payment_time = driver.find_element_by_css_selector(".d-n.SM_pt5>div:nth-of-type(1)>div.mt5")


def main():

	load_driver()

	load_grabr()

	create_order()


if __name__ == '__main__':
	main()
