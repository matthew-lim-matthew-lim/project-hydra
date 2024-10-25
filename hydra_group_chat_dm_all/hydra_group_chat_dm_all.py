""" 
Direct messages (DMs) every member of a provided group chat. 
Helps the user get a response from group chat members.

Takes user input for:
- Group Chat Name
- Message to broadcast to each member (via DMs)

Essential version:
- Messages each member by searching their name in the messenger search box.
"""

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
chrome_options.add_argument("--headless")  # Headless mode means the Chrome window is not displayed

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

target_name = input("Enter Target Group Chat: ")
broadcast_message = input("Enter Message to DM every member: ")

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

    # Search for the group chat
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

    # Wait for the search results to load and find the group chat
    group_chat_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{target_name}']")))
    group_chat_element.click()

    time.sleep(1)

    # Open the group chat members tab to view all the members
    # Wait until the element is present
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Conversation titled CSESOC TECHNICAL EL GRANDE' and @tabindex='0']")))
    element.click()

    time.sleep(3)

    # Wait for the member list to be loaded (adjust the wait time if needed)
    WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), '') and contains(@style, '--lineHeight: 19.9995px;')]")))
    
    # Find all the span elements that contain member names
    member_name_elements = browser.find_elements(By.XPATH, "//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x13faqbe') and contains(@style, '--lineHeight: 19.9995px;')]/span[contains(@class, 'x193iq5w') and contains(@style, 'line-height: 19.9995px;')]")

    # Extract and print the names of all members
    member_names = [element.text for element in member_name_elements if element.text]
    for idx, name in enumerate(member_names, start=1):
        print(f"Member {idx}: {name}")

    # Return to the messenger page
    browser.get("https://www.messenger.com/")
    time.sleep(3)
    
    # Direct Message (DM) Each Member your message
    for member_name in member_names:
        try: 
            # Search for the person
            search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))
            search_box.click()
            search_box.send_keys(member_name)
            search_box.send_keys(Keys.RETURN)  # Press Enter to search

            # Optionally, wait for any overlays to disappear
            try:
                overlay = WebDriverWait(browser, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.__fb-light-mode'))
                )
            except:
                pass  # If there's no overlay, continue

            # Wait for the search results to load and find the person
            person_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{member_name}']")))
            person_element.click()

            # # Wait for the message input box to appear
            # time.sleep(0.1) # Needed, otherwise get a 'StaleElementReferenceException'
            # message_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]')))
            # message_box.click()
            # message_box.send_keys(broadcast_message)  # Type your message
            # time.sleep(0.5)

            # # Send the message by simulating the Enter key
            # message_box.send_keys(Keys.RETURN)
            # time.sleep(0.5)

            # Retry mechanism for sending a message
            attempts = 3
            while attempts > 0:
                try:
                    # Wait for the message input box to appear
                    time.sleep(0.1)  # Needed, otherwise get a 'StaleElementReferenceException'
                    message_box = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]')))
                    message_box.click()
                    message_box.send_keys(broadcast_message)  # Type your message
                    
                    # Send the message by simulating the Enter key
                    message_box.send_keys(Keys.RETURN)
                    time.sleep(0.5)
                    break
                except Exception as e:
                    print(f"Failed to send message: {e}. Retrying...")
                    attempts -= 1
                    time.sleep(5)  # Wait before retrying

        except Exception as e:
            print(f"Failed to send message to {member_name}: {e}")

    print("done!")

    time.sleep(1)


    
