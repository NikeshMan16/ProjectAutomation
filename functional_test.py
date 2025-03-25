import os
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.utils import take_screenshot
import random
import pytest
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
    WebDriverWait(driver, 5).until(EC.url_contains("inventory"))

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

def test_add_to_cart_items_count(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/inventory.html")
    driver.maximize_window()
    time.sleep(2)
    add_to_cart_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Add to cart')]")
    expected_count = len(add_to_cart_buttons)
    for button in add_to_cart_buttons:
        button.click()
        time.sleep(1.5)
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    actual_count = int(cart_badge)
    time.sleep(1)
    try:
        assert actual_count == expected_count, f"Expected {expected_count} items in cart, but found {actual_count}"
    except AssertionError as e:
        take_screenshot(driver)
        pytest.fail(str(e))

def test_remove_from_cart_count(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/inventory.html")
    driver.maximize_window()
    time.sleep(2)
    remove_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Remove')]")
    expected_count = 6 - len(remove_buttons)
    for button in remove_buttons:
        button.click()
        time.sleep(1.5)

    time.sleep(2)  # Give time for elements to render
    try:
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    except NoSuchElementException:
        cart_badge = "0"  # If the element is missing, assume cart is empty
    assert int(cart_badge) == expected_count, f"Cart count mismatch: expected {expected_count}, got {cart_badge}"

    time.sleep(8)


def test_verify_added_cart_items(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/inventory.html")
    time.sleep(2)
    reset_app_state(setup)
    time.sleep(2)
    inventory_items = driver.find_elements(By.CLASS_NAME, 'inventory_item')
    add_to_cart_buttons = driver.find_elements(By.XPATH, '//button[contains(text(),"Add to cart")]')

    if len(inventory_items) >= 2 and len(add_to_cart_buttons) >= 2:
        selected_items = random.sample(list(zip(inventory_items, add_to_cart_buttons)), k=2)
    else:
        pytest.fail("Not enough inventory items found on the page.")
    selected_item_names = []
    for item, button in selected_items:
        item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        selected_item_names.append(item_name)
        button.click()
        time.sleep(1)
    # Navigate to cart page
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(2)
    # Extract item names from the cart
    cart_items = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    cart_item_names = [item.text for item in cart_items]
    # Assert the selected items match the cart items
    assert set(selected_item_names) == set(
        cart_item_names), f"Mismatch: Expected {selected_item_names}, but got {cart_item_names}"


