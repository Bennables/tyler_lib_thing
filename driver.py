from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import timedelta
import datetime
from config import TOKEN


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

    '''
    AVAILABLE SHOULD BE SPLIT BY ROOM, AND THEN SORTED BY TIME AND SPLIT BY BLOCKS(MORE THAN 30 MINS BOOKED)
    '''



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
    consec = 2
    first_available_set = find_consec(available, consec)
    wait(10)

    #     driver.find_element(f"//a[@title='{first_available_set}']").click()
    print(first_available_set)
    for i in first_available_set:
        print(i.get_attribute("title"))
    # print(available)

    for i in range(0, len(first_available_set), 2):
        element = available[i]
        print(element)
        element.click()
        wait(5)
    wait(5)

    button = driver.find_element(by= By.CLASS_NAME, value = 'btn-primary')
    wait(5)
    button.click()
    wait(5)
    button = driver.find_element(by= By.ID, value = 'terms_accept')
    wait(5)
    button.click()
    # for i in ground:
    #     print(i)
    wait(5)
    text_boxes = driver.find_elements(by= By.CLASS_NAME, value = 'form-control')
    for i in range(len(text_boxes)):
        # print(text_boxes[i].get_attribute("placeholder"))
        if text_boxes[i].get_attribute('placeholder') == 'First Name':
            text_boxes = text_boxes[i:i+4]
            break

    for i in text_boxes:
        print(i.get_attribute("name"))

    text = input("First Last Email Label")
    answers = text.split(' ')
    for i in range(4):
        text_boxes[i].send_keys(answers[i])
    wait(5)

    print("JFDKLFSKDJFLKDSJFD")
    print("F:DJKFSLKDFJLSDKJFLKDFJLKDJFLKDSFJLK")