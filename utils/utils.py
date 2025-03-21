import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import inspect

@pytest.fixture(scope="module")
def setup():
    service = Service("driver/chromedriver.exe")
    driver =webdriver.Chrome(service= service)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


def take_screenshot(driver):
    test_name = inspect.currentframe().f_back.f_code.co_name  # GET THE FUNCTION NAME
    screenshot_name = f"screenshots/{test_name}_{int(time.time())}.png"
    driver.save_screenshot(screenshot_name)
    print(f"Screenshot saved: {screenshot_name}")