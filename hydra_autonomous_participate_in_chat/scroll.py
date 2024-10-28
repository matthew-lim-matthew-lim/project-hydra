from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the webdriver (make sure to specify the correct path for your webdriver)
driver = webdriver.Chrome()

# Open a webpage
driver.get("https://neetcode.io/practice")

time.sleep(1)

driver.execute_script("window.scrollBy(0, 1000);")

time.sleep(3)

# Close the browser after testing
driver.quit()