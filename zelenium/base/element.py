from zelenium.base.page import BasePage
from zelenium.exceptions import BaseElementWrongUsageException


class BaseElement:
    page = None

    def __init__(self, by, value):
        self.by = by
        self.value = value
        self.selector = (self.by, self.value)

    def __get__(self, instance, owner):
        if not issubclass(owner, BasePage):
            raise BaseElementWrongUsageException(
                "BaseElement should be used only as "
                "a parameter of BasePage child class"
            )
        self.page = instance
        return self

    def __call__(self):
        return self._find(self.selector)

    def _find(self, selector, parent=None):
        return self.page.wait(parent).until(self.page.dec(selector))

    def child(self, value):
        if isinstance(value, BaseElement):
            value = value.selector
        return self._find(value, self())
