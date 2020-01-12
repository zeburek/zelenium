from selenium.webdriver.support.wait import WebDriverWait

from zelenium import expected_conditions as EC


class BasePage:
    dec = default_expected_condition = None
    dwt = default_wait_time = 5
    dpf = default_poll_frequency = 0.3

    def __init__(
        self,
        driver,
        default_expected_condition=EC.presence_of_element_located,
        default_wait_time=dwt,
        default_poll_frequency=dpf,
    ):
        self.d = self.driver = driver
        self.dec = self.default_expected_condition = default_expected_condition
        self.dwt = self.default_wait_time = default_wait_time
        self.dpf = self.default_poll_frequency = default_poll_frequency

    def wait(self, parent=None):
        return WebDriverWait(parent or self.d, self.dwt, self.dpf)

    def until(self, method, message="", **kwargs):
        return self.wait(**kwargs).until(method, message)

    def until_not(self, method, message="", **kwargs):
        return self.wait(**kwargs).until_not(method, message)
