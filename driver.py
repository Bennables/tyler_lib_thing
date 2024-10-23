from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime


def wait(secs:int):
    time.sleep(secs)

def find_consec(avail : list, consec: int):
    for b in range(len(avail)):
        name1 = avail[b].get_attribute('title').split(' - ')[1]
        for j in range(b, b + consec):
            try:
                name2 = avail[j].get_attribute('title').split(' - ')[1]
                print(f'comparing {name1} to {name2}')
                if name1 == name2 and j == b+consec-1:
                    return avail[b].get_attribute("title")
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
        if starts:
            #removing ground floors and adding them to another list.
            ground.append(available[i])
            available.remove(available[i])
            i-=1
        i+=1

    first_available_set = find_consec(available, 4)
    print(first_available_set)
    wait(10)
    # if first_available_set:
    #     driver.find_element(f"//a[@title='{first_available_set}']").click()
    available = driver.find_elements(by = By.CLASS_NAME, value = "s-lc-eq-avail")

    for i in range(len(available)):
        if available[i].get_attribute("title") == first_available_set:
            element = available[i]
            element.click()
    wait(10)
    # for i in ground:
    #     print(i)

