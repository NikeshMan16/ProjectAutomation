import os
from selenium import webdriver
from selenium.common import TimeoutException
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
    time.sleep(2)

def reset_app_state(setup): # Only works when a user is logged in
    driver = setup
    time.sleep(1)
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,'react-burger-menu-btn'))).click()
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,'reset_sidebar_link'))).click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'react-burger-cross-btn'))).click()

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
    # Find all "Add to cart" buttons
    add_to_cart_buttons = driver.find_elements(By.XPATH, "//button[contains(text(),'Add to cart')]")
    expected_count = len(add_to_cart_buttons)  # Get the number of available products
    for button in add_to_cart_buttons:   # Click all "Add to Cart" buttons
        button.click()
        time.sleep(1.5)  # Ensure UI updates
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text # Retrieve and validate cart count
    actual_count = int(cart_badge)
    time.sleep(1)
    # driver.find_element(By.ID,'shopping_cart_container').click()
    # time.sleep(3)
    try:
        assert actual_count == expected_count, f"Expected {expected_count} items in cart, but found {actual_count}"
    except AssertionError as e:
        take_screenshot(driver)
        pytest.fail(str(e))



def test_verify_added_cart_items(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/inventory.html")
    time.sleep(2)
    reset_app_state(setup)
    time.sleep(2)
    # Finding all the inventory items and their names
    inventory_items = driver.find_elements(By.CLASS_NAME,'inventory_item')
    add_to_cart_buttons = driver.find_elements(By.XPATH,'//button[contains(text(),"Add to Cart")]')

    #Select random items to add to Cart
    selected_items = random.sample(list(zip(inventory_items,add_to_cart_buttons)),k=3)
    added_items = []

    for item,button in selected_items:
        item_name = item.find_element(By.CLASS_NAME,'inventory_item_name').text
        added_items.append(item_name)
        button.click()
        time.sleep(1)  #Wait for the UI update

    # Navigate to Cart
    driver.find_element(By.ID,'shopping_cart_container').click()
    time.sleep(2)

    #Verify add items are displayed in the cart
    cart_items = driver.find_elements(By.CLASS_NAME,'inventory_item_name')
    cart_items_name = [item.text for item in cart_items]

    try:
        assert set(added_items) == set(cart_items_name) , f"Mismatch in cart items, Expected items:{added_items}, but found {cart_items_name}"
    except AssertionError as e:
        take_screenshot(driver)
        pytest.fail(str(e))









