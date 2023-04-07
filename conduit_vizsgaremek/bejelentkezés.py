from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

service = Service(executable_path=ChromeDriverManager().install())
options = Options()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=service, options=options)
URL = "http://localhost:1667/"
browser.get(URL)
browser.maximize_window()

# Bejelentkezés funkció ellenőrzése üres mező kitöltéssel

sing_in_page_button = browser.find_element(By.XPATH, '//a[@href="#/login"]')
sing_in_page_button.click()

email_input = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
email_input.send_keys()
password_input = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
password_input.send_keys()

sing_in_button = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
sing_in_button.click()

time.sleep(2)

login_message = browser.find_element(By.XPATH, '//div[@class="swal-title"]')
login_problem = browser.find_element(By.XPATH, '//div[@class="swal-text"]')
assert login_message.text == "Login failed!"
assert login_problem.text == "Email field required."

login_failed_button = browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
login_failed_button.click()

# Bejelentkezés funkció ellenőrzése helytelen adattal (jelszó)

email_input = browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
email_input.send_keys('tesztelo0124@gmail.com')
password_input = browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
password_input.send_keys('Tesztelek')

sing_in_button = browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
sing_in_button.click()

time.sleep(2)

login_message = browser.find_element(By.XPATH, '//div[@class="swal-title"]')
login_problem = browser.find_element(By.XPATH, '//div[@class="swal-text"]')
assert login_message.text == "Login failed!"
assert login_problem.text == "Invalid user credentials."

login_failed_button = browser.find_element(By.XPATH, '//button[@class="swal-button swal-button--confirm"]')
login_failed_button.click()

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
