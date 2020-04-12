from string import Formatter
from typing import Tuple
from typing import Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from zelenium import expected_conditions as EC
from zelenium.base.config import Config


class FormatTuple(tuple):
    def __getitem__(self, key):
        if key + 1 > len(self):
            return "{}"
        return tuple.__getitem__(self, key)


class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def f(string, *args, **kwargs):
    formatter = Formatter()
    args_mapping = FormatTuple(args)
    mapping = FormatDict(kwargs)
    return formatter.vformat(string, args_mapping, mapping)


class Base:
    conf: Config = None

    def __init__(self, conf: Config = None):
        self.conf = conf or Config.get_instance()

    def wait(self, parent: WebDriver = None):
        return WebDriverWait(
            parent or self.conf.d, self.conf.dwt, self.conf.dpf
        )

    def find(
        self,
        selector: Union[Tuple[str, str], "BaseElement"],
        parent: WebDriver = None,
    ):
        if isinstance(selector, BaseElement):
            selector = selector.selector
        return self.wait(parent).until(self.conf.dec(selector))

    def find_all(
        self,
        selector: Union[Tuple[str, str], "BaseElement"],
        parent: WebDriver = None,
    ):
        if isinstance(selector, BaseElement):
            selector = selector.selector
        return self.wait(parent).until(
            EC.presence_of_all_elements_located(selector)
        )


class BaseElement(Base):
    by: str
    value: str
    selector: Tuple[str, str]
    _suffix: str = ""

    def __init__(self, by: str, value: str):
        super().__init__()
        self.by = by
        self.value = value

    def __call__(self):
        return self.find(self.selector)

    def __repr__(self):
        return "Element {1} ({0})".format(*self.selector)

    @property
    def selector(self):
        return self.by, f(self.value, s=self._suffix)

    def set_suffix(self, value):
        self._suffix = value

    def format(self, *args, **kwargs):
        el = BaseElement(self.by, f(self.value, *args, **kwargs))
        el.set_suffix(self._suffix)
        return el

    def child(self, value: Union[Tuple[str, str], "BaseElement"]):
        return self.find(value, self())

    def child_all(self, value: Union[Tuple[str, str], "BaseElement"]):
        return self.find_all(value, self())

    def all(self):
        return self.find_all(self.selector)
