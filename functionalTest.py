import os
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.utils import take_screenshot

os.makedirs("screenshots", exist_ok=True)

@pytest.fixture(scope="module")
def setup():
    service = Service("driver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

def login_function(setup):
    driver = setup
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,'user-name'))).send_keys("standard_user")
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,'password'))).send_keys("secret_sauce")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID,'login-button'))).click()
    time.sleep(2)

def test_navigation_to_cart(setup):
    driver = setup
    login_function(setup)
    time.sleep(1)
    driver.find_element(By.ID,'shopping_cart_container').click()
    time.sleep(2)
    try:
        assert "cart" in driver.current_url, "Failed to navigate to cart"
    except AssertionError as e:
        print(f"Assertion Failed : {e}")
        take_screenshot(driver)
        pytest.fail(str(e))

def test_navigation_from_cart_to_inventory(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/cart.html")
    time.sleep(2)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID,'continue-shopping'))).click()
    time.sleep(2)
    try:
        assert  "inventory" in driver.current_url,"Continue shopping button functionality failed."
    except AssertionError as e:
        print(f"Assertion failed: {e}")
        pytest.fail(str(e))

# def add_to_cart_button_functionality(setup):
#     driver = setup
#     driver.get("https://www.saucedemo.com/inventory.html")
#     time.sleep(2)
#     add_to_cart_buttons = driver.find_elements(By.XPATH,"//button[contains(text(),'Add to cart')]")
#     for button in add_to_cart_buttons:
#         button.click()
#         time.sleep(1)
#


