"""
WIP (INCOMPLETE/NOT WORKING)

Autonomous Chat Participation

Using ChatGPT or other language model

I guess you could make this run the messaging every 24 hours (with a bit of randomisation to make it look more natural),
leaving the program running on a server. 
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
import json
from openai import OpenAI
from selenium.common.exceptions import WebDriverException

def is_driver_active(driver):
    try:
        # Try to retrieve the current URL, which is a simple command.
        driver.current_url
        return True
    except WebDriverException as e:
        # If an exception occurs, it means the driver is dead or disconnected.
        print(f"Driver is not active: {e}")
        return False
    
# Helper removes characters that aren't in the BMP (since selenium can't send non-BMP characters)
def remove_non_bmp_characters(text):
    # Iterate through the text, keeping only BMP characters
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

# Load .env file
load_dotenv()
fb_messenger_username = os.getenv('FB_MESSENGER_USERNAME')
fb_messenger_password = os.getenv('FB_MESSENGER_PASSWORD')
fb_messenger_pin = os.getenv('CHAT_HISTORY_PIN')

# Set up OpenAI API Key
openai_client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")  # You can add this back if you want to run it in headless mode

# Reduce detection of automation
chrome_options.add_argument("--disable-blink-features=AutomationControlled")   # adding argument to disable the AutomationControlled flag 
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])   # exclude the collection of enable-automation switches 
chrome_options.add_experimental_option("useAutomationExtension", False)    # turn-off userAutomationExtension 
driver = webdriver.Chrome(options=chrome_options)  # setting the driver path and requesting a page 
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") # changing the property of the navigator value for webdriver to undefined 

# Define paths
user_home_dir = os.path.expanduser("~")
chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

# Set binary location and service
chrome_options.binary_location = chrome_binary_path
service = Service(chromedriver_path)

# Get the name of the target
target_name = input("Input Target Person/Groupchat Name: ")

# Set up logging for the target chat
file_path = 'chat_log.json'

# Load existing chat log if it exists
if os.path.exists(file_path):
    with open(file_path, 'r') as json_file:
        chat_log = json.load(json_file)
else:
    chat_log = {}  # Start with an empty log

# Ensure we have a list for this target chat
if target_name not in chat_log:
    chat_log[target_name] = []

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

    ### ###

    # Restart here
    scrape_success = False 

    message_containers = []

    while not scrape_success:
        if not is_driver_active(browser):
            print("Driver is dead. Relaunching...")
            browser.quit()  # Clean up the old browser
            browser = driver = webdriver.Chrome(options=chrome_options)  # Reinitialize the browser
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            browser.get("https://www.messenger.com/")

        try:
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

            ### ###

            #####
            # Get all the messages in the chat
            # Optionally, wait for any overlays to disappear
            try:
                overlay = WebDriverWait(browser, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.__fb-light-mode'))
                )
            except:
                pass  # If there's no overlay, continue

            time.sleep(0.1)

            # browser.execute_script("window.scrollBy(0, 1000);")

            # Logic to identify messages
            message_containers = browser.find_elements(By.XPATH, "//div[contains(@class, '__fb-light-mode') and @role='row']")

            scrape_success = True
        except:
            pass 

    for container in message_containers:
        # Identify sender
        sender = ""
        if sender == "":
            try:
                sender_info = container.find_element(By.XPATH, ".//span[contains(text(), 'You sent')]")
                sender = "You"
            except:
                pass
        if sender == "":
            try:
                sender_info = container.find_element(By.XPATH, ".//span[contains(@class, 'html-span')]")
                sender = sender_info.text  # Should give the other person's name
            except:
                pass
        if sender == "":
            try:
                reply_element = container.find_element(By.XPATH, ".//span[contains(text(), 'replied to')]")
                if "You replied to " in reply_element.text:
                    sender = "You"
                else:
                    sender = reply_element.text.split()[0]
            except:
                pass

        # Extract and print the message text
        # try:
        #     message_text = container.find_element(By.XPATH, ".//div[@dir='auto']").text
        #     print(f"{sender}: {message_text}")
        # except:
        #     print(f"{sender}: [No message text found]")

        try:
            # Try to find the message text element
            message_text = container.find_element(By.XPATH, ".//div[@dir='auto']").text
            print(f"{sender}: {message_text}")
        except:
            try:
                # If the text element is not found, try getting the aria-label attribute of the <a> element.
                # This is usually when a facebook post is sent or forwarded to a group chat.
                message_text = container.find_element(By.TAG_NAME, "a").get_attribute("aria-label")
                if message_text:
                    print(f"{sender}: {message_text}")
                else:
                    message_text = "[No message text or aria-label found]"
                    print(f"{sender}: [No message text or aria-label found]")
            except:
                message_text = "[No message text or aria-label found]"
                print(f"{sender}: [No message text or aria-label found]")

        message_entry = {"sender": sender, "text": message_text}
        # Check if this message is already in the log
        if message_entry not in chat_log[target_name]:
            # print(f"New message found: {sender}: {message_text}")
            chat_log[target_name].append(message_entry)

    with open(file_path, 'w') as json_file:
        json.dump(chat_log, json_file, indent=4)

    #####
    regenerate = True

    while regenerate:
        # Determine if it is our turn to send a message, and what message we should send. 
        if chat_log[target_name]:
            # At the moment, we can simply check who sent the last message.
            if chat_log[target_name][-1]["sender"] != "You":
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are the user 'You'. Send a reply message to the other people, and ask a follow up question if you think its appropriate. "
                            "Your tone should be tiny bit informal, spontaneous, and tiny bit playful. "
                            "Sometimes use shorthand expressions and emojis. Lowercase text."
                            "Respond naturally to topics, showing genuine interest and empathy. Nonchalant. Neutral language."
                            "I prefer something that feels more natural, grounded, authentic. Clear and straightforward language."
                            "No emojis allowed."
                            "Normally each message is short, so a sentance over multiple messages."
                            "You may add a mature minimalist touch of humor or encouragement where appropriate, and keep your messages brief"
                            "Use '\n' for seperate messages. Just send the raw text messages, no annotations required. DO NOT USE \" or \'."
                            "Example for how to format reply: yep\nidrk but i reckon we should play golf\nand\nget maccas after"
                        )
                    },
                    {
                        "role": "user",
                        "content": json.dumps(chat_log[target_name], indent=4)
                    }
                ]

                response = openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=messages
                )

                response.choices[0].message.content = remove_non_bmp_characters(response.choices[0].message.content)

                print("ChatGPT Generated Message, Array Form:")
                print(response.choices[0].message.content.split('\n'))

                # Actually, the program will exit if niether Y or R are sent
                ok_to_send = input("Is this okay to send? ('Y' to send, 'R' to regenerate response, 'N' to exit program): ")

                if ok_to_send == "Y":
                    for message_to_send in response.choices[0].message.content.split('\n'):
                        # Wait for the message input box to appear
                        time.sleep(0.1) # Needed, otherwise get a 'StaleElementReferenceException'
                        message_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]')))
                        message_box.click()
                        message_box.send_keys(message_to_send)  # Type your message
                        message_box.send_keys(Keys.RETURN)  # Send the message by simulating the Enter key
                    print("Messages Sent")

                    regenerate = False 
                elif ok_to_send != "R":
                    break
                elif ok_to_send == "R":
                    print("Regenerating Message")
                    
        # Maybe make it so that it counts down until sending, and the user can interrupt it and modify the message, or can ask for the message
        # to be regenerated.

    print("Exiting Program")

    time.sleep(1)

    
