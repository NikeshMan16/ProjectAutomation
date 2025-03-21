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

# List of usernames with unique test case IDs
usernames = [
    ('TC_001', 'standard_user'),
    ('TC_002', 'problem_user'),
    ('TC_003', 'performance_glitch_user'),
    ('TC_004', 'error_user'),
    ('TC_005', 'visual_user'),
    ('TC_006', 'locked_out_user')
]

@pytest.mark.parametrize("test_case_id, username", usernames)
def test_login_valid_user(setup, test_case_id, username):
    driver = setup
    password = "secret_sauce"

    try:
        un = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'user-name')))
        un.clear()  # Clear field before entering data
        un.send_keys(username)
        time.sleep(2)

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
        time.sleep(2)

        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'login-button'))).click()
        time.sleep(3)

        assert "inventory" in driver.current_url, f"Failed Login for {test_case_id}"

    except AssertionError as e:
        print(f"Assertion Error in {test_case_id}: {e}")
        take_screenshot(driver)
        pytest.fail(str(e))

    except TimeoutException:
        print(f"Timeout Error in {test_case_id}: Too long time to load / performance issues.")
        take_screenshot(driver)

    finally:
        # Logout before running the next test case
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, 'react-burger-menu-btn'))).click()
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, 'logout_sidebar_link'))).click()
        except TimeoutException:
            print(f"Logout timeout for {test_case_id}")
            take_screenshot(driver)
