from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def wait(secs:int):
    time.sleep(secs)


driver = webdriver.Chrome()
driver.get("https://calendar.library.ucsc.edu/spaces")
wait(2)



