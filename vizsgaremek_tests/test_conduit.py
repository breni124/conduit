import time
import csv
# import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from basic_functions import login, new_article
from data_import import user_data, article, modified_article


class TestConduit(object):

    def setup_method(self):
        s = Service(executable_path=ChromeDriverManager().install())
        o = Options()
        o.add_experimental_option("detach", True)
        #o.add_argument('--headless')
        o.add_argument('--no-sandbox')
        o.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(service=s, options=o)

        URL = "http://localhost:1667/#/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        # time.sleep(1)
        self.browser.quit()

    # 1 Regisztráció helyes adatokkal ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_registration(self):
        signup_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href="#/register"]')
        signup_button.click()
        time.sleep(2)

        username_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Username"]')))
        email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        confirm_signup = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        username_input.send_keys(user_data['username'])
        email_input.send_keys(user_data['email'])
        password_input.send_keys(user_data['password'])
        confirm_signup.click()

        registration_confirmed = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="swal-title"]')))
        time.sleep(1)

        assert registration_confirmed.text == "Welcome!"


    # Regisztráció helytelen adatokkal

    def test_registration1(self):
        sign_up_button = self.browser.find_element(By.LINK_TEXT, 'Sign up')
        sign_up_button.click()

        username_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        email_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Email"]')
        password_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')

        username_input.send_keys(user_data["username"])
        email_input.send_keys('tesztelo@')
        password_input.send_keys(user_data["password"])

        sign_up_button2 = self.browser.find_element(By.XPATH, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        sign_up_button2.click()

        registration_message = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
        registration_problem = self.browser.find_element(By.XPATH, '//div[@class="swal-text"]')
        assert registration_message.text == "Registration failed!"
        assert registration_problem.text == "Email must be a valid email."

        registration_failed_button = self.browser.find_element(By.XPATH,
                                                               '//button[@class="swal-button swal-button--confirm"]')
        registration_failed_button.click()

    # 2 Bejelentkezés ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_login(self):

        signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
        signin_button.click()

        email_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Email"]')))
        password_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]')))
        confirm_signin = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-lg btn-primary pull-xs-right"]')))

        email_input.send_keys(user_data['email'])
        password_input.send_keys(user_data['password'])
        confirm_signin.click()
        time.sleep(5)

    # Ellenőrzés

        profile = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/nav/div/ul/li[4]/a')))
        assert profile.is_displayed
        assert profile.text == user_data['username']

    # 3 Adatkezelési nyilatkozat----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_data_cookies(self):
        # Ellenőrzés

        cookie_policy_panel = self.browser.find_element(By.ID, 'cookie-policy-panel')
        assert cookie_policy_panel.is_displayed()

        # Elfogadás gomb kikeresése, megnyomása

        accept_cookies_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        time.sleep(1)
        accept_cookies_btn.click()
        time.sleep(1)

        # Ellenőrzés

        assert len(self.browser.find_elements(By.ID, 'cookie-policy-panel')) == 0

    # 4 Adatok listázása ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_list_data(self):
        login(self.browser)

        popular_tags = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div/div/a[@class="tag-pill tag-default"]')))

        tags = []
        for tag in popular_tags:
            tags.append(tag.text)
        # print(tags)

        assert len(tags) != 0

    # 5 Több oldalas lista bejárása----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_all_pages(self):

        login(self.browser)

        page_links_list = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="pagination"]/li/a')))
        for page_link in page_links_list:
            page_link.click()
            time.sleep(2)
            actual_page = self.browser.find_element(By.CSS_SELECTOR, 'li[class="page-item active"]')

        # Ellenőrzés

            assert page_link.text == actual_page.text


    # 6 Új adat bevitel ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_new_data(self):

        login(self.browser)

        # Új bejegyzés létrehozása

        new_article_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
        time.sleep(1)
        new_article_btn.click()

        title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        about_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
        full_article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
        tags_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))
        submit_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

        title_input.send_keys(article['title'])
        about_input.send_keys(article['about'])
        full_article_input.send_keys(article['article'])
        tags_input.send_keys(article['tags'])
        submit_button.click()

        # Helyes létrehozás, ellenőrzés

        h1_title = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        assert h1_title.text == article['title']

  #  7 Ismételt és sorozatos adatbevitel adatforrásból----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_read_data(self):

        login(self.browser)

        # csv megnyitása

        with open('vizsgaremek_tests/articles.csv', 'r', encoding='UTF-8') as file:
            articles = csv.reader(file, delimiter=';')
            next(articles)

            # Lista létrehozása
            title_list = []

            # csv fájl soraihoz mezők kikeresése
            for row in articles:
                new_article_btn = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@href="#/editor"]')))
                time.sleep(1)
                new_article_btn.click()

                title_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
                about_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
                article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
                tags_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))
                submit_button = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

                title_list.append(row[0])

                title_input.send_keys(row[0])
                about_input.send_keys(row[1])
                article_input.send_keys(row[2])
                tags_input.send_keys(row[3])
                submit_button.click()

            # Ellenőrzés, kezdőoldalon

            home_btn = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
            home_btn.click()

            time.sleep(2)

            for title in title_list:
                assert (self.browser.find_element(By.PARTIAL_LINK_TEXT, f'{title}')).is_displayed()

    # 8 Meglévő adat módosítás ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_modify_data(self):

        login(self.browser)

        new_article(self.browser)


        edit_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="btn btn-sm btn-outline-secondary"]')))
        edit_button.click()

        title_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Article Title"]')))
        about_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="What\'s this article about?"]')))
        article_input = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea[placeholder="Write your article (in markdown)"]')))
        tags_input = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter tags"]')))
        submit_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

        title_input.clear()
        about_input.clear()
        article_input.clear()
        title_input.send_keys(modified_article['title'])
        about_input.send_keys(modified_article['about'])
        article_input.send_keys(modified_article['article'])
        tags_input.send_keys(modified_article['tags'])
        submit_button.click()
        time.sleep(1)

        home_btn = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="#/"]')))
        home_btn.click()
        time.sleep(2)

        assert self.browser.find_element(By.PARTIAL_LINK_TEXT, f'{modified_article["title"]}').is_displayed()

    #  9 Adat vagy adatok törlése ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_delete_data(self):

        login(self.browser)

        new_article(self.browser)

        article_url = self.browser.current_url
        delete_article_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//i[@class="ion-trash-a"]')))
        delete_article_button.click()

        time.sleep(5)

        assert self.browser.current_url != article_url

        # 10 Adatok lementése felületről ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_write_data(self):

        login(self.browser)

        popular_tags = WebDriverWait(self.browser, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div/div/a[@class="tag-pill tag-default"]')))

        tags = []
        for tag in popular_tags:
            tags.append(tag.text)
        print(tags)

        with open('tags', 'w', encoding="UTF-8") as tag_file:
            tag_file.write(str(tags))

        # 11 Kijelentkezés----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_logout(self):

        login(self.browser)

        # Kijelentkezés

        logout_button = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Log out')))
        logout_button.click()
        time.sleep(1)

        signin_button = self.browser.find_element(By.CSS_SELECTOR, 'a[href = "#/login"]')
        assert signin_button.is_displayed()
