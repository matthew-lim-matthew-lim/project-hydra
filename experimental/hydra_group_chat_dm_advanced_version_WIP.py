""" 
WIP (INCOMPLETE/NOT WORKING)

Direct messages (DMs) every member of a provided group chat. 
Helps the user get a response from group chat members.

Takes user input for:
- Group Chat Name
- Message to broadcast to each member (via DMs)

Advanced Version:
- Retreives message link from members list, meaning that the member DMed is precisely the one in the group chat guaranteed.
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
# chrome_options.add_argument("--headless")  # You can add this back if you want to run it in headless mode

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

target_name = "CSESOC TECHNICAL EL GRANDE"

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
    person_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{target_name}']")))
    person_element.click()

    # Open the group chat members tab to view all the members
    # Wait until the element is present
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Conversation titled CSESOC TECHNICAL EL GRANDE' and @tabindex='0']")))
    element.click()


    # Find members using their class names
    time.sleep(0.1)
    members = browser.find_elements(By.CSS_SELECTOR, 'div[class="x1qjc9v5 x9f619 x78zum5"]')

    # Iterate through each member and send a message
    for member in members:
        try:
            # Extract the member's name (you can adjust this part to match the exact structure)
            member_name = member.find_element(By.CSS_SELECTOR, 'span[class="x193iq5w"]').text
            print(f"Sending message to {member_name}")
            
            # Click on the message button
            message_button = member.find_element(By.CSS_SELECTOR, '[aria-label^="Message"]')
            message_button.click()
            
            # Wait for message window to open
            time.sleep(2)
            
            # Type and send the message (modify based on your exact message box structure)
            # Wait for the message input box to appear
            time.sleep(0.1) # Needed, otherwise get a 'StaleElementReferenceException'
            message_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]')))
            message_box.click()
            message_box.send_keys("Hii, are you going to come to technical bnb on the 1st of November? "
                                "If you can go I would be so happy! And I'll miss you otherwise") 

            # Send the message by simulating the Enter key
            # message_box.send_keys(Keys.RETURN)
            
            # Wait after sending the message
            time.sleep(2)
            
            # Close the chat or navigate back to the member list
            # You might need to automate closing the message window or going back
            
        except Exception as e:
            print(f"Failed to send message to {member_name}: {e}")

        # Wait for the message input box to appear
        time.sleep(0.1) # Needed, otherwise get a 'StaleElementReferenceException'
        message_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]')))
        message_box.click()
        # message_box.send_keys("yea")  # Type your message

        # Send the message by simulating the Enter key
        # message_box.send_keys(Keys.RETURN)

        print("done!")

        time.sleep(1)

    
