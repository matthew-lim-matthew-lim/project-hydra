"""
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
import readline
import sys
from selenium.common.exceptions import TimeoutException
import random
from datetime import datetime
from zoneinfo import ZoneInfo

# Helper determines if the driver is active or not
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

# Helper sends the messages to the chat
def send_messages(messages_array):
    for message_to_send in messages_array:
        # Wait for the message input box to appear
        time.sleep(0.1) # Needed, otherwise get a 'StaleElementReferenceException'
        message_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-label="Message"]')))
        message_box.click()
        message_box.send_keys(message_to_send)  # Type your message
        message_box.send_keys(Keys.RETURN)  # Send the message by simulating the Enter key

# Define the restricted hours (24-hour format)
RESTRICTED_START = 2  # 2 AM
RESTRICTED_END = 6    # 6 AM

# Restricted hours ensure we don't send messages during cooked hours
def is_in_restricted_hours():
    current_hour = datetime.now(ZoneInfo("Australia/Sydney")).hour
    print(f"The current time is: {current_hour}")
    return current_hour > RESTRICTED_START and current_hour < RESTRICTED_END

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

# Set up logging for the target chat
file_path = 'chat_log.json'

# No-reply count: The number of no-replies before double-texting. Default is 40.
init_no_reply_count = 40

# Are we okay with double-texting, haha rip :(
double_text = False 
if len(sys.argv) > 1:
    if sys.argv[1] == "dt":
        double_text = True
    elif sys.argv[1].isdigit():
        # If the 1st argument is a number, it is the number of no-replies before double-texting
        init_no_reply_count = int(sys.argv[1])

no_reply_count = init_no_reply_count

# Load existing chat log if it exists
if os.path.exists(file_path):
    with open(file_path, 'r') as json_file:
        chat_log = json.load(json_file)
else:
    chat_log = {}  # Start with an empty log

# How often do we want to send messages?
hrs_between_messages = float(input("How many hours in between each message cycle? (Decimals accepted): "))

# Collect configuration information for chat targets
targets_info = []

# User Input:
# [User/Chat to Target],[Partial Name Match (Y/N)],[Chat Goals/Topics (can be empty)]
try:
    while True:
        target_info = {
            "target_name": "",
            "partial_match": False,
            "chat_goals": ""
        }
        print("Enter Details of Users/Chats to target in the following format.")
        print("[User/Chat to Target]\[Partial Name Match (Y/N)]\[Chat Goals/Topics (can be empty)]")
        user_input = input("Your input (type 'q' or press Ctrl+C to stop): ")
        if user_input == "q":
            raise Exception("quit")
        user_input_parsed = user_input.split("\\")
        target_info["target_name"] = user_input_parsed[0]
        if user_input_parsed[1] == "Y":
            target_info["partial_match"] = True
        target_info["chat_goals"] = user_input_parsed[2]
        print(f"You entered: {target_info}")
        targets_info.append(target_info)

        # Add target name to chat log if it was not already there
        if target_info["target_name"] not in chat_log:
            chat_log[target_info["target_name"]] = []
except:
    print("\nInput completed, activating Hydra in Hardcore Mode")

while True:
    if is_in_restricted_hours():
        print("Current time is within restricted hours. Waiting until allowed to send messages.")
        print(f"The configured restricted hours are between {RESTRICTED_START} and {RESTRICTED_END} (24 hour time).")
        # Wait for an hour before checking again to save resources
        time.sleep(3600)
        continue

    print("\nStarting Hydra Cycle. Put your seatbelts on!\n")
    # Initialize Chrome WebDriver
    with webdriver.Chrome(options=chrome_options) as browser:
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

        for target_info in targets_info:
            # Restart here
            target_name = target_info["target_name"]

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
                    # Search for the person/chat
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

                    # # Wait for the search results to load and find the person/chat
                    try:
                        # Try to find the exact match
                        person_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li//span[text()='{target_name}']")))
                        person_element.click()

                    except TimeoutException:
                        # If exact match is not found, use partial match if that option was selected
                        if target_info["partial_match"]:
                            try:
                                # Find and click the partial match
                                person_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li//span[contains(text(), '{target_name}')]")))
                                person_element.click()
                                print("Partial match found!")
                            except TimeoutException:
                                print(f"No partial match found for '{target_name}' either.")
                                continue  # Terminate sending for the current person

                        else:
                            print("No match selected.")
                            continue

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
            
            # Determine if it is our turn to send a message, and what message we should send. 
            if chat_log[target_name]:
                if chat_log[target_name][-1]["sender"] != "You":
                    no_reply_count -= 1
                # Send message if it is our turn to reply, or if we want to double_text
                if chat_log[target_name][-1]["sender"] != "You" or double_text or no_reply_count == 0:
                    no_reply_count = init_no_reply_count
                    messages = [
                        {
                            "role": "system",
                            "content": (
                                "You are the user 'You'. Send a reply message to the other people, and ask a follow up question if you think its appropriate. "
                                "Lowercase text."
                                "Nonchalant. Neutral language."
                                "I prefer something that feels more natural, grounded, authentic. Clear and straightforward language."
                                "No emojis allowed."
                                "Normally each message is short, so a sentance over multiple messages."
                                "Only respond to maybe the last 10 messages or so, and if you have already responded to a particular message, take account of that."
                                "You may add a mature minimalist touch of humor or encouragement where appropriate, and keep your messages brief"
                                "The following is extremely important: "
                                "Use '\n' for seperate messages. Just send the raw text messages, no annotations required. DO NOT USE \" or \'."
                                "Example for how to format reply: yep\nidrk but i reckon we should play golf\nand\nget maccas after"
                                # Extra stuff for hydra hardcore mode
                                "You have an overall goal/topic for this chat, which you might work towards over a large number of messages."
                                "Don't make it too forceful. You will go several messages without talking about the goal/topic."
                                "The goal/topic is as follows:"
                                + target_info["chat_goals"]
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

                    # In hardcore mode, we just send it! No checking necessary hahaha!
                    send_messages(response.choices[0].message.content.split('\n'))
                            
                # Maybe make it so that it counts down until sending, and the user can interrupt it and modify the message, or can ask for the message
                # to be regenerated.

            print("Completed sending for ", target_name)

            time.sleep(1)

    print("\nHydra cycle Complete. Wait for next Hydra cycle has been inititated.")
    wait_time = hrs_between_messages * 60 * 60 + random.randint(0, 3600)
    print("The wait time is " + str(wait_time / (60 * 60)) + " hours.")
    time.sleep(wait_time)