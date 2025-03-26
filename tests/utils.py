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


def login_function(setup):
    driver = setup
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,'user-name'))).send_keys("standard_user")
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,'password'))).send_keys("secret_sauce")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID,'login-button'))).click()
    WebDriverWait(driver, 5).until(EC.url_contains("inventory"))

def logout_function(setup):
    driver = setup
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,'react-burger-menu-btn'))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID,'logout_sidebar_link'))).click()

def reset_app_state(setup):
    driver = setup
    time.sleep(1)
    menu_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'react-burger-menu-btn')))
    menu_button.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'reset_sidebar_link')))
    reset_button = driver.find_element(By.ID, 'reset_sidebar_link')
    driver.execute_script("arguments[0].scrollIntoView(true);", reset_button)
    time.sleep(1)
    reset_button.click()
    close_menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'react-burger-cross-btn')))
    close_menu.click()