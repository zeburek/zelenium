import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from zelenium import expected_conditions as EC
from zelenium.base.config import _Config
from zelenium.base.page import BasePage


def test_default_ec_and_wait_time(driver, serve):
    class Page(BasePage):
        pass

    conf = _Config(driver, EC.visibility_of_element_located, 1, 0.5)
    page = Page(conf)
    start = time.time()
    with pytest.raises(TimeoutException):
        page.wait().until(page.conf.dec((By.CSS_SELECTOR, ".no-link")))
    assert (time.time() - start) < 1.3


def test_default_poll_frequency(driver, serve):
    class Page(BasePage):
        pass

    inc = 0

    def ec(_):
        def action(_):
            nonlocal inc
            inc += 1
            return False

        return action

    conf = _Config(driver, ec, 1, 0.2)
    page = Page(conf)
    with pytest.raises(TimeoutException):
        page.wait().until(page.conf.dec(None))
    assert inc == 5


def test_wait_until(driver, serve):
    class Page(BasePage):
        pass

    conf = _Config(driver, EC.visibility_of_element_located, 1, 0.5)
    page = Page(conf)
    body = page.until(page.conf.dec((By.TAG_NAME, "body")))
    assert body.tag_name == "body"
    with pytest.raises(TimeoutException):
        page.until(page.conf.dec((By.CSS_SELECTOR, ".no-link")), parent=body)


def test_wait_until_not(driver, serve):
    class Page(BasePage):
        pass

    conf = _Config(driver, EC.visibility_of_element_located, 1, 0.5)
    page = Page(conf)
    body = page.until(page.conf.dec((By.TAG_NAME, "body")))
    assert body.tag_name == "body"
    no_elem = page.until_not(
        page.conf.dec((By.CSS_SELECTOR, ".no-link")), parent=body
    )
    assert not no_elem
