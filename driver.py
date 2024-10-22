from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def wait(secs:int):
    time.sleep(secs)


driver = webdriver.Chrome()
driver.get("https://calendar.library.ucsc.edu/spaces")
wait(10)

available = driver.find_elements(by = By.CLASS_NAME, value = "s-lc-eq-avail")

print(available)
