# zelenium
New Selenium framework for Python with base pages and elements

# Installation

```bash
pip install zelenium
```

# Usage

Zelenium offers several features that could be combined with classical
selenium usage:

* Driver singleton configuration;
* BasePage with BaseElements;
* Suffix and formatting mechanisms for BaseElements;
* It also should be useful for Appium testing.

## zelenium configuration

To setup configuration for zelenium you could just use `Config`:

```python
from selenium import webdriver
from zelenium import Config

config = Config.get_instance()
config.driver = webdriver.Chrome()
```

Because Config is singleton - you could not use it with two different
webdrivers at one moment. But if you need it, you could use private class:

```python
from zelenium import Config
from zelenium.base.config import _Config

config1 = Config.get_instance()
config2 = _Config()

assert not (config1 is config2)  # No assertion
```

## BasePage and BaseElement

What offers you BasePage:

* No need to pass webdriver instance - it would be passed from
configuration automatically
* Some predefined methods, which are useful in testing
* Suffix mechanism

### Define new Page

Let's imagine that we have already setup webdriver for Config,
and starting to create new page:

```python
from selenium.webdriver.common.by import By
from zelenium import BasePage

class LoginPage(BasePage):
    title = (By.CSS_SELECTOR, "[data-test='title']")
    username = (By.CSS_SELECTOR, "[data-test='username']")
    password = (By.CSS_SELECTOR, "[data-test='password']")
    submit = (By.CSS_SELECTOR, "[data-test='submit']")

def main():
    login_page = LoginPage()
    print(login_page.title().text)

main()
```

If we execute it after opening something in browser - it will find
element and print text inside of it.

How it works?

Well, BasePage also has a `metaclass` that will go all over page class
fields and if field is tuple with two strings - it would replace it with
`BaseElement`.

`BaseElement` itself has magic `__call__` method,  which executes when
you 'call' class instance:
```python
from zelenium import BE
elem = BE("by", "selector")
web_element = elem()  # Here you calls class instance and it will return
                      # WebElement for you. Just classic WebElement
```

### Inherit pages

For example, you have several pages, which have same structure, but some
different logic, for example:

```python
from selenium.webdriver.common.by import By
from zelenium import BasePage

class LoginPage(BasePage):
    title = (By.CSS_SELECTOR, "[data-test='title']")
    username = (By.CSS_SELECTOR, "[data-test='username']")
    password = (By.CSS_SELECTOR, "[data-test='password']")
    submit = (By.CSS_SELECTOR, "[data-test='submit']")

    def login(self, username, password):
        self.username().send_keys(username)
        self.password().send_keys(password)
        self.submit().click()


class RegisterPage(LoginPage):
    full_name = (By.CSS_SELECTOR, "[data-test='full_name']")

    def register(self, full_name, username, password):
        self.full_name().send_key(full_name)
        self.username().send_keys(username)
        self.password().send_keys(password)
        self.submit().click()
```

Using this - you have no need to redefine elements on different pages -
you could just inherit them, if they have same locators (or quite the same).

### Format elements

Sometimes you need to define a lot of elements with similar locators.
Zelenium offers two way to solve this. First is BaseElement formatting:

```python
from selenium.webdriver.common.by import By
from zelenium import BasePage, BE

class DevicesPage(BasePage):
    _cell = BE(By.CSS_SELECTOR, "[data-test='devicesPageCell_{}']")
    user = _cell.format("user")
    imei = _cell.format("imei")
    iccid = _cell.format("iccid")
    model = _cell.format("model")
```

`.format()` method formats locator as a string and returns new instance
of BaseElement.

Second mechanism is suffix:

```python
from selenium.webdriver.common.by import By
from zelenium import BasePage

class DevicesPage(BasePage):
    __suffix = "devicesPageCell_"
    user = (By.CSS_SELECTOR, "[data-test='{s}_user']")
    imei = (By.CSS_SELECTOR, "[data-test='{s}_imei']")
    iccid = (By.CSS_SELECTOR, "[data-test='{s}_iccid']")
    model = (By.CSS_SELECTOR, "[data-test='{s}_model']")
```

Main differences of this two mechanisms are:

* Suffix adds to locator automatically;
* Suffix could be inherited;
* Format could be used anywhere outside classes - you could format
element in some functions according to changes on page.
* Format requires usage of BaseElement class itself

Example of suffix inheritance:

```python
from selenium.webdriver.common.by import By
from zelenium import BasePage


class LoginPage(BasePage):
    __suffix = "loginPageForm_"

    title = (By.CSS_SELECTOR, "[data-test='{s}title']")
    username = (By.CSS_SELECTOR, "[data-test='{s}username']")
    password = (By.CSS_SELECTOR, "[data-test='{s}password']")
    submit = (By.CSS_SELECTOR, "[data-test='{s}submit']")


class RegisterPage(LoginPage):
    __suffix = "registerPageForm_"

    email = (By.CSS_SELECTOR, "[data-test='{s}email']")
    confirm = (By.CSS_SELECTOR, "[data-test='{s}confirm']")


class RenamedRegisterPage(RegisterPage):
    __suffix = "renamedRegisterPageForm_"


def main():
    log = LoginPage()
    reg = RegisterPage()
    ren = RenamedRegisterPage()

    print(log.title)
    print(log.username)
    print(log.password)
    print(log.submit)
    print(reg.title)
    print(reg.username)
    print(reg.password)
    print(reg.submit)
    print(reg.email)
    print(reg.confirm)
    print(ren.title)
    print(ren.username)
    print(ren.password)
    print(ren.submit)
    print(ren.email)
    print(ren.confirm)


if __name__ == '__main__':
    main()
```

This code will output:

```text
Element [data-test='loginPageForm_title'] (css selector)
Element [data-test='loginPageForm_username'] (css selector)
Element [data-test='loginPageForm_password'] (css selector)
Element [data-test='loginPageForm_submit'] (css selector)
Element [data-test='registerPageForm_title'] (css selector)
Element [data-test='registerPageForm_username'] (css selector)
Element [data-test='registerPageForm_password'] (css selector)
Element [data-test='registerPageForm_submit'] (css selector)
Element [data-test='registerPageForm_email'] (css selector)
Element [data-test='registerPageForm_confirm'] (css selector)
Element [data-test='renamedRegisterPageForm_title'] (css selector)
Element [data-test='renamedRegisterPageForm_username'] (css selector)
Element [data-test='renamedRegisterPageForm_password'] (css selector)
Element [data-test='renamedRegisterPageForm_submit'] (css selector)
Element [data-test='renamedRegisterPageForm_email'] (css selector)
Element [data-test='renamedRegisterPageForm_confirm'] (css selector)
```
