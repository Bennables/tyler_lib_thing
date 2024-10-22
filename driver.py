from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime


def wait(secs:int):
    time.sleep(secs)

def find_consec(avail : list, consec: int):
    for b in range(len(avail)):
        for j in range(b, b + consec):
            try:
                name = avail[j].get_attribute('title').split(' - ')[1]
                print(name)
            except:
                #this would only trigger when out of range of available
                return None


if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.get("https://calendar.library.ucsc.edu/spaces")
    wait(10)

    available = driver.find_elements(by = By.CLASS_NAME, value = "s-lc-eq-avail")
    # for i in available:
        # print(i.get_attribute("title").split(' ')[0])

    available = sorted(available, key = lambda index : (index.get_attribute("title")[index.get_attribute('title').index('-') + 2:], datetime.datetime.strptime(index.get_attribute("title").split(' ')[0], "%I:%M%p")))
    # for i in available:
    #     print(i.get_attribute("title"))
    # print(available)

    #when you book a slot, if there's one immediately after, it, it auto chooses that one too.
    #tyler doesn't want the ground floors
    ground = []
    i = 0
    while i < len(available):
        starts = available[i].get_attribute("title")[available[i].get_attribute('title').index('-') + 2:].startswith("Ground")
        print(starts)
        if starts:
            #removing ground floors and adding them to another list.
            ground.append(available[i])
            available.remove(available[i])
            i-=1
        i+=1

    find_consec(available, 1)
    # for i in available:
    #     print(i.get_attribute("title"))
    #
    # for i in ground:
    #     print(i)

