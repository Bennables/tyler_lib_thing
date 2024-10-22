from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import re


def wait(secs:int):
    time.sleep(secs)


driver = webdriver.Chrome()
driver.get("https://calendar.library.ucsc.edu/spaces")
wait(10)

available = driver.find_elements(by = By.CLASS_NAME, value = "s-lc-eq-avail")
for i in available:
    print(i.get_attribute("title").split(' ')[0])

available = sorted(available, key = lambda index : ( datetime.datetime.strptime(index.get_attribute("title").split(' ')[0], "%I:%M%p"), index.get_attribute("title")[13:]))
for i in available:
    print(i.get_attribute("title"))
print(available)
#a