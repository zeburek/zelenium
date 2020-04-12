from typing import Callable

from zelenium.base import Base
from zelenium.base import BaseElement


class MetaPage(type):
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        suffix = attrs.get("_{}__suffix".format(name), "")
        for base in bases:
            for name, val in base.__dict__.items():
                if isinstance(val, BaseElement):
                    attrs[name] = (val.by, val.value)
        for name, value in attrs.items():
            if isinstance(value, tuple) and len(value) == 2:
                by, selector = value
                value = BaseElement(by, selector)
                value.set_suffix(suffix)
            new_attrs[name] = value
        return super().__new__(cls, name, bases, new_attrs)


class BasePage(Base, metaclass=MetaPage):
    __suffix = ""

    def until(self, method: Callable, message: str = "", **kwargs):
        return self.wait(**kwargs).until(method, message)

    def until_not(self, method: Callable, message: str = "", **kwargs):
        return self.wait(**kwargs).until_not(method, message)
