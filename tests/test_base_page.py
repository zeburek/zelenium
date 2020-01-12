import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from zelenium import expected_conditions as EC
from zelenium.base.page import BasePage


def test_access_default_attributes(driver):
    class Page(BasePage):
        pass

    page = Page(
        driver=driver,
        default_expected_condition=EC.visibility_of_element_located,
        default_wait_time=2,
        default_poll_frequency=0.5,
    )
    assert page.d == page.driver == driver
    assert (
        page.dec
        == page.default_expected_condition
        == EC.visibility_of_element_located
    )
    assert page.dwt == page.default_wait_time == 2
    assert page.dpf == page.default_poll_frequency == 0.5


def test_default_ec_and_wait_time(driver, serve):
    class Page(BasePage):
        pass

    page = Page(driver, EC.visibility_of_element_located, 1, 0.5)
    start = time.time()
    with pytest.raises(TimeoutException):
        page.wait().until(page.dec((By.CSS_SELECTOR, ".no-link")))
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

    page = Page(driver, ec, 1, 0.2)
    with pytest.raises(TimeoutException):
        page.wait().until(page.dec(None))
    assert inc == 5


def test_wait_until(driver, serve):
    class Page(BasePage):
        pass

    page = Page(driver, EC.visibility_of_element_located, 1, 0.5)
    body = page.until(page.dec((By.TAG_NAME, "body")))
    assert body.tag_name == "body"
    with pytest.raises(TimeoutException):
        page.until(page.dec((By.CSS_SELECTOR, ".no-link")), parent=body)


def test_wait_until_not(driver, serve):
    class Page(BasePage):
        pass

    page = Page(driver, EC.visibility_of_element_located, 1, 0.5)
    body = page.until(page.dec((By.TAG_NAME, "body")))
    assert body.tag_name == "body"
    no_elem = page.until_not(
        page.dec((By.CSS_SELECTOR, ".no-link")), parent=body
    )
    assert not no_elem
