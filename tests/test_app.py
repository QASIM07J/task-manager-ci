from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get("http://127.0.0.1:5000")

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=6)) + "@test.com"

try:
    print("✅ Test 1: Home Page Title")
    assert "Task Manager" in driver.title
    print("Title is:", driver.title)

    print("✅ Test 2: Navigate to Sign Up")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign up here"))

    ).click()
    # Wait for the signup form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    assert "Sign Up" in driver.page_source

    print("✅ Test 3: Valid Registration")
    driver.find_element(By.NAME, "username").send_keys("testuser")
    email = random_email()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "confirm_password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    # Wait for login form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    assert "Login" in driver.page_source

    print("✅ Test 4: Login Success")
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "submit").click()
    # Wait for dashboard (task form) to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )
    assert "Welcome" in driver.page_source or "Dashboard" in driver.page_source

    print("✅ Test 5: Add Task")
    driver.find_element(By.NAME, "title").send_keys("Selenium Test Task")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Selenium Test Task")
    )
    assert "Selenium Test Task" in driver.page_source

    print("✅ Test 6: Mark Task Complete")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mark Complete')]"))
    ).click()
    time.sleep(1)

    print("✅ Test 7: Delete Task")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Delete')]"))
    ).click()
    time.sleep(1)

    print("✅ Test 8: Logout")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    assert "Login" in driver.page_source

except Exception as e:
    print("❌ Test failed:", e)
    print(driver.page_source)  # Print page source for debugging

finally:
    driver.quit()