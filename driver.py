from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import timedelta
import datetime
from config import TOKEN
import csv


def wait(secs:int):
    time.sleep(secs)

def find_consec(avail : list, consec: int):
    #initialize array to hold on to good times
    good_times = []
    #loop thru avail
    for b in range(len(avail)):
        #resetting the list bc hasn't been found
        good_times = []
        #gets the room name
        name1 = avail[b].get_attribute('title').split(' - ')[1]
        time1 =  datetime.datetime.strptime(avail[b].get_attribute("title").split(' ')[0], "%I:%M%p")
        for j in range(b, b + consec):
            try:
                #gets the second room name
                name2 = avail[j].get_attribute('title').split(' - ')[1]
                #gets teh second time
                time2 = datetime.datetime.strptime(avail[j].get_attribute("title").split(' ')[0], "%I:%M%p")
                #makes sure the time slots are consecutive
                time_change = time2-time1 < timedelta(minutes = 31)
                print(f'comparing {name1} to {name2}')
                #checking
                if name1 == name2 and time_change:
                    good_times.append(avail[j])
                    #updates time1 to compare next loop
                    time1 = time2
                    #returns the list if found enough consecutive time slots in same room
                    if len(good_times) == consec:
                        print("Found a good room.")
                        return good_times
                else:
                    break
            except:
                #this would only trigger when out of range of available
                return []
    return good_times

def create_driver():
    driver = webdriver.Chrome()
    print(type(driver))
    driver.get("https://calendar.library.ucsc.edu/spaces")
    return driver

def find_available_times(driver):
    available = driver.find_elements(by = By.CLASS_NAME, value = "s-lc-eq-avail")
    return sorted(available, key = lambda index : (index.get_attribute("title")[index.get_attribute('title').index('-') + 2:], datetime.datetime.strptime(index.get_attribute("title").split(' ')[0], "%I:%M%p")))

def remove_ground_floors(available):
    #tyler doesn't want any ground floors. I think I"ll make it so that he'll get ground floors if there are no upper floors available.
    # ground = []
    i = 0
    while i < len(available):
        starts = available[i].get_attribute("title")[available[i].get_attribute('title').index('-') + 2:].startswith("Ground")
        if starts:
            #removing ground floors and adding them to another list.
            # ground.append(available[i])
            available.remove(available[i])
            i-=1
        i+=1
    return available

def loop_print(arr):
    for i in arr:
        print(i.get_attribute("title"))
    # print(available)

def click_times(first_available_set):
    for i in range(0, len(first_available_set), 2):
        element = first_available_set[i]
        print(element)
        element.click()
        wait(5)

def click_stuff(driver):
    button = driver.find_element(by= By.CLASS_NAME, value = 'btn-primary')
    wait(2)
    button.click()
    wait(2)
    button = driver.find_element(by= By.ID, value = 'terms_accept')
    wait(2)
    button.click()
    # for i in ground:

def find_text_boxes(driver):
    text_boxes = driver.find_elements(by= By.CLASS_NAME, value = 'form-control')
    for i in range(len(text_boxes)):
        # print(text_boxes[i].get_attribute("placeholder"))
        if text_boxes[i].get_attribute('placeholder') == 'First Name':
            text_boxes = text_boxes[i:i+3]
            return text_boxes
        
def fill_form(user):
    with open('accounts.csv', 'r') as file:
        reader = csv.reader(file)
        row = [row for row in reader]
        for i in row:
            if i[0] == user:
                return i
    return None

def check_user(user):
    # try:
    with open('accounts.csv', 'r') as file:
        reader = csv.reader(file)
        row = [row for row in reader]
        for i in row:
            if i[0] == user:
                return True
    return False

        

def book_it(user, consec):
    if check_user(user):
        driver = create_driver()
        wait(5)
        available = find_available_times(driver)
        wait(2)
        available = remove_ground_floors(available)
        first_available_set = find_consec(available, consec)
        wait(3)
        loop_print(first_available_set)
        click_times(first_available_set)
        click_stuff(driver)
        text_boxes = find_text_boxes(driver)
        values = fill_form(user)
        wait()
        if values:
            for i in range(3):
                text_boxes[i].send_keys(values[i])
            wait (10)
            return (0, 0)
        else:
            return 2
    else:
        return 2