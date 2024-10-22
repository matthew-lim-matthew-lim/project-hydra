from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time

# Load .env file
load_dotenv()
fb_messenger_username = os.getenv('FB_MESSENGER_USERNAME')
fb_messenger_password = os.getenv('FB_MESSENGER_PASSWORD')
fb_messenger_pin = os.getenv('CHAT_HISTORY_PIN')

# Define Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")  # You can add this back if you want to run it in headless mode

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

target_name = "Brandon Tan"

# Initialize Chrome WebDriver
with webdriver.Chrome(service=service, options=chrome_options) as browser:
    # Open Messenger login page
    browser.get("https://www.messenger.com/")

    # Wait for the login form to be visible
    wait = WebDriverWait(browser, 15)
    login_form = wait.until(EC.visibility_of_element_located((By.ID, "loginform")))

    # Find and interact with the email and password fields
    email_box = wait.until(EC.element_to_be_clickable((By.NAME, "email")))
    email_box.send_keys(fb_messenger_username)

    password_box = wait.until(EC.element_to_be_clickable((By.NAME, "pass")))
    password_box.send_keys(fb_messenger_password)

    # Click the login button
    login_submit = wait.until(EC.element_to_be_clickable((By.ID, "loginbutton")))
    login_submit.click()

    # Optionally wait for the next page (Messenger home) to load
    # Wait for the PIN input box if required (depending on whether PIN is requested after login)
    pin_box = wait.until(EC.presence_of_element_located((By.ID, "mw-numeric-code-input-prevent-composer-focus-steal")))
    pin_box.send_keys(fb_messenger_pin)


    # Wait until the PIN box disappears
    wait.until(EC.invisibility_of_element_located((By.ID, "mw-numeric-code-input-prevent-composer-focus-steal")))

    # Optionally, wait for any overlays to disappear
    try:
        overlay = WebDriverWait(browser, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.__fb-light-mode'))
        )
    except:
        pass  # If there's no overlay, continue

    # Search for the person
    search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))
    search_box.click()
    search_box.send_keys(target_name)
    search_box.send_keys(Keys.RETURN)  # Press Enter to search

    # Optionally, wait for any overlays to disappear
    try:
        overlay = WebDriverWait(browser, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.__fb-light-mode'))
        )
    except:
        pass  # If there's no overlay, continue

    # Wait for the search results to load and find the person
    person_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{target_name}']")))
    person_element.click()

    # Wait for the message input box to appear
    time.sleep(0.1) # Needed, otherwise get a 'StaleElementReferenceException'
    message_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]')))
    message_box.click()
    message_box.send_keys("yea")  # Type your message

    # Send the message by simulating the Enter key
    message_box.send_keys(Keys.RETURN)

    print("done!")

    time.sleep(1)

    
