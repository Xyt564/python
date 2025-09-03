from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time, random

# ------------------- Setup -------------------
driver_path = "/media/xyt564/sd_card/python/new/selenium/geckodriver"
service = Service(driver_path)

options = Options()
# options.headless = True  # keep GUI visible for less bot detection
options.add_argument("--width=1200")
options.add_argument("--height=800")

# Create profile and set user agent
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
options.profile = profile  # attach profile to Options object

driver = webdriver.Firefox(service=service, options=options)

driver.get("https://www.google.com")

# ------------------- Accept Cookies -------------------
try:
    accept_button = driver.find_element(By.XPATH, "//button//*[text()='Accept all']/..")
    accept_button.click()
    time.sleep(random.uniform(1, 2))
except:
    print("No consent popup or already accepted.")

# ------------------- Human-like Search -------------------
search_box = driver.find_element(By.NAME, "q")
actions = ActionChains(driver)

query = "Python programming"
for char in query:
    search_box.send_keys(char)
    time.sleep(random.uniform(0.08, 0.18))  # random delay per character

time.sleep(random.uniform(0.5, 1.5))
search_box.submit()

# ------------------- Click First Result -------------------
time.sleep(random.uniform(2, 4))
try:
    first_result = driver.find_element(By.XPATH, "//div[@id='search']//a")
    actions.move_to_element(first_result).pause(random.uniform(0.3, 0.7)).click(first_result).perform()
except:
    print("Could not click first result.")

# ------------------- Optional: scroll page slowly -------------------
for i in range(3):
    driver.execute_script("window.scrollBy(0, window.innerHeight/3);")
    time.sleep(random.uniform(1, 2))

# ------------------- Done -------------------
time.sleep(5)
driver.quit()
