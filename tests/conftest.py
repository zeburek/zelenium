import os

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def driver():
    remote_host = os.getenv("SELENIUM_HOST", None)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    if remote_host:
        chrome_options.add_argument("--single-process")
        driver = webdriver.Remote(
            remote_host, desired_capabilities=chrome_options.to_capabilities()
        )
    else:
        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            chrome_options=chrome_options,
        )
    yield driver
    driver.quit()


@pytest.fixture
def serve(driver, httpserver):
    path = os.path.join(os.getcwd(), "tests", "pages", "index.html")
    httpserver.serve_content(open(path).read())
    driver.get(httpserver.url)
