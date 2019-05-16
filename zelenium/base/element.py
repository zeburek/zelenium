from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class BaseDriver:
    dec = default_expected_condition = None
    dwt = default_wait_tim = 0

    def __init__(
        self,
        driver: WebDriver,
        default_expected_condition=EC.presence_of_element_located,
        default_wait_time=5,
    ):
        self.d = self.driver = driver
        self.dec = default_expected_condition
        self.dwt = default_wait_time

    def find_element(self, by: By, selector, wait_time=dwt):
        pass
