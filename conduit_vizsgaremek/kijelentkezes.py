import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=service, options=options)
URL = "http://localhost:1667/"
browser.get(URL)
browser.maximize_window()

# Bejelentkezés funkció ellenőrzése helyes adatokkal

sign_in_page_button = browser.find_element(By.XPATH, '//a[@href="#/login"]')
sign_in_page_button.click()

email_input = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
email_input.clear()
email_input.send_keys('tesztelo0124@gmail.com')
password_input = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
password_input.clear()
password_input.send_keys('Tesztelek2023')

sign_in_button = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
sign_in_button.click()

time.sleep(2)

user_profile = browser.find_elements(By.XPATH, '//a[@class="nav-link"]')[2]
assert user_profile.text == 'tesztelo0124'


# Kijelentkezés funkció ellenőrzése

log_out_button = browser.find_element(By.XPATH, '//a[@active-class="active"]')
log_out_button.click()

time.sleep(2)

sign_in_page_button = browser.find_element(By.XPATH, '//a[@href="#/login"]')
assert sign_in_page_button.is_displayed()