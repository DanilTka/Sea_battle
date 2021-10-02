from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait



class JSTest(StaticLiveServerTestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # delete for more safe testing
        file = 'C:/Program Files (x86)/django-sites/sea_battle_prod/backend/game/tests/func_tests/selenium/chromedriver.exe'
        self.driver = webdriver.Chrome(
            file,
            options=options
        )
        webdriver_login(self.driver,
                        username='testing',
                        password='12345test',
                        live_server_url=self.live_server_url
                        )

    def test_fields_presence(self):
        self.driver.get(self.live_server_url + '/game/room_test')
        self.driver.find_element_by_id("099")
        self.driver.find_element_by_id("199")
        self.driver.find_element_by_id("chat-log")
        self.driver.find_element_by_id("chat-message-input")

    def test_chat(self):
        self.driver.get(self.live_server_url + '/game/room_test')
        self.driver.find_element_by_id("chat-log")
        input = self.driver.find_element_by_id("chat-message-input")
        input.clear()
        input.send_keys("hello", Keys.ENTER)
        wait_until(my_driver=self.driver, timeout=2)
        self.driver.find_elements_by_xpath("//*[contains(text(), 'hello')]")

    def test_gameplay_js(self):
        self.driver.get(self.live_server_url + '/game/room_test')
        self.driver.find_element_by_id("100").click()
        wait_until(my_driver=self.driver, timeout=2)
        message_hint = self.driver.find_element_by_id("message-hint")
        self.assertEqual(message_hint.text, "Opponent's turn")

    def test_find_opponent_but(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_name("find_opponent").click()
        wait_until(my_driver=self.driver, timeout=2)

    def tearDown(self):
        self.driver.quit()


def webdriver_login(driver, username, password, live_server_url):
    """
    Login test user.
    """
    driver.get(live_server_url)
    username_field = driver.find_element_by_name("username")
    password_field = driver.find_element_by_name("password")
    submit = driver.find_element_by_class_name("submit-button")
    username_field.clear()
    password_field.clear()
    username_field.send_keys(username)
    password_field.send_keys(password)
    submit.click()


def wait_until(my_driver, timeout):
    """
    Waits until the page is loaded.
    """
    WebDriverWait(my_driver, timeout).until(
        lambda driver: driver.find_element_by_tag_name('body'))
