from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import timedelta
import datetime
from config import TOKEN
import csv

git p
def wait(secs:int):
    time.sleep(secs)

def find_consec(avail : list, consec: int):
    # #initialize array to hold on to good times
    # timeframes = []
    # times = []

    # for b in range(len(avail) - 1):
        
    #     time1 =  datetime.datetime.strptime(avail[b].get_attribute("title").split(' ')[0], "%I:%M%p")
    #     time2 = datetime.datetime.strptime(avail[b + 1].get_attribute("title").split(' ')[0], "%I:%M%p")
    #     name1 = avail[b].get_attribute('title').split(' - ')[1]
    #     name2 = avail[b+1].get_attribute('title').split(' - ')[1]
    #     time_change = time2-time1 < timedelta(minutes = 31)
    #     if time_change and name1 == name2:
    #         if not times:
    #             times.append(avail[b])
    #         times.append(avail[b+1])
    #     else:
    #         timeframes.append(times)
    #         times = []
        

    # i = 0
    # while i < len(timeframes):
    #     if len(timeframes[i]) < consec:
    #         timeframes.remove(timeframes[i])
    #         print('removed')
    #         i-=1
    #     i += 1


    # for i in range(len(timeframes)):
    #     loop_print(timeframes[i])
    # sorted = sorted(
    #     timeframes,
    #     key=lambda index: datetime.datetime.strptime(
    #         index[0].get_attribute("title").split(' - ')[0].split(' ')[0].upper(),
    #         "%I:%M%p"
    #     )
    # )
    # for i in range(len(sorted)):
    #     print("NEW ONE")
    #     for j in range(len(sorted[i])):
    #         print(sorted[i][j].get_attribute("title"))

        



    '''
    parse the dates and put them into lists based on consecutive
    put into lists, if len isn't greater than this, remove it
    sort by time on start.


    '''


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
        element.click()
        wait(2)

def remove_bad_times(available, time, consec):
    available2 = []
    i=0
    while i < len(available):
        current = datetime.datetime.strptime(available[i].get_attribute("title").split(' ')[0], "%I:%M%p")
        reference_date = time
        # Change the year, month, and day of `first_date` to match `reference_date`
        current = current.replace(year=reference_date.year, month=reference_date.month, day=reference_date.day)
        if  current >= time:
            available2.append(available[i])
        i+=1
    return available2

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

def start_and_end(driver):
    # start = first_available_set[0].get_attribute("title")
    # end = first_available_set[-1].get_attribute("title")
    # print(start, end)
    return ''

def book_it(user, consec, time, days_ahead = 0):
    finished_string = ''
    if check_user(user):
        driver = create_driver()
        wait(3)

        for i in range(days_ahead):
            next = driver.find_element(by = By.CLASS_NAME, value = 'fc-next-button')
            next.click()
            wait(2)

        available = find_available_times(driver)

        available = remove_ground_floors(available)
        available = remove_bad_times(available, time, consec)
        try:
            first_available_set = find_consec(available, consec)
            wait(2)
            click_times(first_available_set)
            click_stuff(driver)
            text_boxes = find_text_boxes(driver)
            values = fill_form(user)
            finished_string += start_and_end(driver)
            wait(2)
            if values:
                for i in range(3):
                    text_boxes[i].send_keys(values[i])
                wait (10)
                return (0, 0)
            else:
                return 2
        except:
            return 4
    else:
        return 2