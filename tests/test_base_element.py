import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from zelenium import expected_conditions as EC
from zelenium.base.element import BaseElement
from zelenium.base.page import BasePage
from zelenium.exceptions import BaseElementWrongUsageException


def test_access_default_attributes():
    class Page(BasePage):
        elem = BaseElement("test", "value")

    page = Page(None)
    assert page.elem.by == "test"
    assert page.elem.value == "value"
    assert page.elem.selector == ("test", "value")


@pytest.mark.parametrize("by,value,tag_name", [
    (By.TAG_NAME, "body", "body"),
    (By.CLASS_NAME, "parent", "div"),
    (By.ID, "parent-div", "div"),
    (By.CSS_SELECTOR, ".parent", "div"),
    (By.LINK_TEXT, "Link with text", "a"),
    (By.XPATH, "//div[@class='parent']", "div"),
])
def test_base_element_by(driver, serve, by, value, tag_name):
    class Page(BasePage):
        elem = BaseElement(by, value)
    page = Page(driver)
    elem = page.elem()
    assert elem
    assert elem.tag_name == tag_name


@pytest.mark.parametrize("by,value,tag_name", [
    (By.TAG_NAME, "div", "div"),
    (By.CLASS_NAME, "parent", "div"),
    (By.ID, "parent-div", "div"),
    (By.CSS_SELECTOR, ".parent", "div"),
    (By.LINK_TEXT, "Link with text", "a"),
    (By.XPATH, ".//div[@class='parent']", "div"),
])
def test_base_child_element_by(driver, serve, by, value, tag_name):
    class Page(BasePage):
        body = BaseElement(By.TAG_NAME, "body")
        elem = BaseElement(by, value)
    page = Page(driver)
    elem = page.body.child(page.elem)
    assert elem
    assert elem.tag_name == tag_name


def test_default_expected_condition(driver, serve):
    class Page(BasePage):
        link = BaseElement(By.CSS_SELECTOR, ".no-link")

    page = Page(driver, EC.visibility_of_element_located, 1, 0.5)
    with pytest.raises(TimeoutException):
        page.link()


def test_base_element_wrong_usage_exception():
    class Page:
        elem = BaseElement("test", "val")
    with pytest.raises(BaseElementWrongUsageException):
        page = Page()
        page.elem()
