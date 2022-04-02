import unittest

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class E2eTests(unittest.TestCase):
    def setUp(self):
        self.chrome_driver = "./chromedriver/chromedriver"
        self.chrome_service = Service(self.chrome_driver)
        self.chrome_options = Options()
        self.chrome_options.add_argument("--incognito")
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            service=self.chrome_service, options=self.chrome_options
        )
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        self.driver.quit()

    def test_browser_title_contains_app_name(self):
        self.assertIn("Named Entity", self.driver.title)

    def test_page_heading_is_named_entity_finder(self):
        heading = self.find_elements(
            self.driver, './/h1[@data-test-id="heading"]', True
        )
        self.assertEqual("Named Entity Finder", heading.text)

    def test_page_has_input_for_text(self):
        input_element = self.find_elements(
            self.driver, './/input[@data-test-id="input-text"]', True
        )
        self.assertIsNotNone(input_element)

    def test_page_has_button_for_submitting_text(self):
        submit_button = self.find_elements(
            self.driver, './/input[@data-test-id="find-button"]', True
        )
        self.assertIsNotNone(submit_button)

    def test_page_has_ner_table(self):
        input_element = self.find_elements(
            self.driver, './/input[@data-test-id="input-text"]', True
        )
        submit_button = self.find_elements(
            self.driver, './/input[@data-test-id="find-button"]', True
        )
        input_element.send_keys("France and Germany share a border in Europe.")
        submit_button.click()
        table = self.find_elements(
            self.driver, './/table[@data-test-id="ner-table"]', True
        )
        self.assertIsNotNone(table)

    def find_elements(self, driver, xpath, singleton=False, timeout=0):
        WAIT_DEFAULT = 10  # usually 5000 but changed to 10 for testing purposes
        POLL_FREQUENCY = 2
        wait = WebDriverWait(driver, timeout or WAIT_DEFAULT, POLL_FREQUENCY)
        if singleton:
            return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        return wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
