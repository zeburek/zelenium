import logging
from typing import Callable

import attr
from selenium.webdriver.remote.webdriver import WebDriver
from zelenium import expected_conditions as EC
from zelenium.utils.singleton import singleton

logger = logging.getLogger("zelenium")


@attr.s
class _Config:
    driver = attr.ib(default=None, type=WebDriver)
    default_expected_condition = attr.ib(
        default=EC.presence_of_element_located, type=Callable
    )
    default_wait_time = attr.ib(default=5, type=int)
    default_poll_frequency = attr.ib(default=0.3, type=float)

    @property
    def d(self):
        return self.driver

    @property
    def dec(self):
        return self.default_expected_condition

    @property
    def dwt(self):
        return self.default_wait_time

    @property
    def dpf(self):
        return self.default_poll_frequency

    @classmethod
    def get_instance(cls):
        return Config()


Config = singleton(_Config)
