from typing import Callable, Type

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    d: WebDriver
    driver: WebDriver
    dec: Type
    default_expected_condition: Type
    dwt: int
    default_wait_time: int
    dpf: float
    default_poll_frequency: float

    def __init__(
        self, driver: WebDriver,
        default_expected_condition=None,
        default_wait_time: int = None,
        default_poll_frequency: float = None
    ):
        ...

    def wait(self, parent: WebElement = None) -> WebDriverWait:
        ...

    def until(self, method: Callable, message: str = None, **kwargs) -> WebDriverWait.until:
        ...

    def until_not(self, method: Callable, message: str = None, **kwargs) -> WebDriverWait.until_not:
        ...
