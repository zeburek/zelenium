import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from zelenium import expected_conditions as EC
from zelenium.base import BaseElement
from zelenium.base.page import BasePage


def test_access_default_attributes():
    elem = BaseElement("test", "value")

    assert elem.by == "test"
    assert elem.value == "value"
    assert elem.selector == ("test", "value")
    assert repr(elem) == "Element value (test)"


format_params = (
    "suffix, selector, args, valid",
    [
        ("", "selector_{}", (1,), "selector_1"),
        ("1", "{s}_selector", (), "1_selector"),
        ("1", "{s}_selector_{}", (1,), "1_selector_1"),
        ("1", "{s}_selector_{}_{}", (1, 2), "1_selector_1_2"),
    ],
)


@pytest.mark.parametrize(*format_params)
def test_format_element_after_suffix(suffix, selector, args, valid):
    elem = BaseElement("test", selector)
    elem.set_suffix(suffix)
    elem = elem.format(*args)
    assert elem.selector == ("test", valid)


@pytest.mark.parametrize(*format_params)
def test_format_element_before_suffix(suffix, selector, args, valid):
    elem = BaseElement("test", selector)
    elem = elem.format(*args)
    elem.set_suffix(suffix)
    assert elem.selector == ("test", valid)


@pytest.mark.parametrize(
    "by,value,tag_name",
    [
        (By.TAG_NAME, "body", "body"),
        (By.CLASS_NAME, "parent", "div"),
        (By.ID, "parent-div", "div"),
        (By.CSS_SELECTOR, ".parent", "div"),
        (By.LINK_TEXT, "Link with text", "a"),
        (By.XPATH, "//div[@class='parent']", "div"),
    ],
)
def test_base_element_by(driver, serve, by, value, tag_name):
    class Page(BasePage):
        elem = (by, value)

    page = Page()
    elem = page.elem()
    assert elem
    assert elem.tag_name == tag_name


@pytest.mark.parametrize(
    "by,value,tag_name",
    [
        (By.TAG_NAME, "body", "body"),
        (By.CLASS_NAME, "parent", "div"),
        (By.ID, "parent-div", "div"),
        (By.CSS_SELECTOR, ".parent", "div"),
        (By.LINK_TEXT, "Link with text", "a"),
        (By.XPATH, "//div[@class='parent']", "div"),
    ],
)
def test_base_all_elements_by(driver, serve, by, value, tag_name):
    class Page(BasePage):
        elem = (by, value)

    page = Page(driver)
    elem = page.elem.all()
    assert len(elem) == 1
    assert elem[0]
    assert elem[0].tag_name == tag_name


@pytest.mark.parametrize(
    "by,value,tag_name",
    [
        (By.TAG_NAME, "div", "div"),
        (By.CLASS_NAME, "parent", "div"),
        (By.ID, "parent-div", "div"),
        (By.CSS_SELECTOR, ".parent", "div"),
        (By.LINK_TEXT, "Link with text", "a"),
        (By.XPATH, ".//div[@class='parent']", "div"),
    ],
)
def test_base_child_element_by(driver, serve, by, value, tag_name):
    class Page(BasePage):
        body = (By.TAG_NAME, "body")
        elem = (by, value)

    page = Page(driver)
    elem = page.body.child(page.elem)
    assert elem
    assert elem.tag_name == tag_name


@pytest.mark.parametrize(
    "by,value,tag_name",
    [
        (By.TAG_NAME, "div", "div"),
        (By.CLASS_NAME, "parent", "div"),
        (By.ID, "parent-div", "div"),
        (By.CSS_SELECTOR, ".parent", "div"),
        (By.LINK_TEXT, "Link with text", "a"),
        (By.XPATH, ".//div[@class='parent']", "div"),
    ],
)
def test_base_all_child_elements_by(driver, serve, by, value, tag_name):
    class Page(BasePage):
        body = (By.TAG_NAME, "body")
        elem = (by, value)

    page = Page(driver)
    elem = page.body.child_all(page.elem)
    assert len(elem) == 1
    assert elem[0]
    assert elem[0].tag_name == tag_name


def test_default_expected_condition(driver, serve):
    class Page(BasePage):
        link = (By.CSS_SELECTOR, ".no-link")

    page = Page()
    page.conf.default_expected_condition = EC.visibility_of_element_located
    with pytest.raises(TimeoutException):
        page.link()
