from typing import Type, Any, Tuple, Union

from selenium.webdriver.remote.webelement import WebElement

from zelenium.base.page import BasePage


class BaseElement:
    page: BasePage
    by: str
    value: str
    selector: Tuple[str, str]

    def __init__(self, by: str, value: str):
        ...

    def __get__(self, instance: BasePage, owner: Type[BasePage]):
        ...

    def __call__(self) -> WebElement:
        ...

    def _find(
        self, selector: Tuple[str, str], parent: WebElement = None
    ) -> WebElement:
        ...

    def child(self, value: Union[BaseElement, Tuple[str, str]]) -> WebElement:
        ...
