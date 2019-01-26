import os
import time
import requests 
import tkinter as tk
from selenium import webdriver
from sys import platform
import urllib.request
from xml.etree import ElementTree
from selenium.webdriver.support.wait import WebDriverWait
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#BASE_DIR = os.path.dirname("/home/aayushshivam7/")
DRIVER_NAME = "chromedriver.exe" if platform == "win32" else "chromedriver"
DRIVER_DIR = os.path.join(BASE_DIR, "static/plugins", DRIVER_NAME)
converter = "https://www.360converter.com/conversion/video2TextConversion?type=v2t"
duration = '00:00:30'

def wait_for_page_load(driver, timeout=30):
        old_page = driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(driver, timeout).until(
            staleness_of(old_page)
        )

def convert_to_text(filePath, keyword):

    filePath = "/home/priyanshu/Desktop/GTube/static/images/videoplayback.mp4"
    driver = webdriver.Chrome(DRIVER_DIR)
    driver.get(converter)
    radio = driver.find_element_by_id('srcLocal')
    radio.click() 
    
    chooser = driver.find_element_by_id('myfile') 
    chooser.send_keys(filePath) ;
    
    option =  driver.find_element_by_xpath("//select[@name='language']/option[@value='en-US']").click()  
    
    timer = driver.find_element_by_id('to')
    timer.clear()
    timer.send_keys(duration)

    agree = driver.find_element_by_id('agreementCheck') 
    agree.click()
    print(driver.current_url)
    submit = driver.find_element_by_id('StartConvert')
    submit.click()
    element = WebDriverWait(driver, 60).until(
        lambda x: x.find_element_by_id("finished"))
    
    new_driver = driver.window_handles[0]
    print(driver.current_url)

    driver.switch_to_window(new_driver)
    button = driver.find_element_by_id('downloadlink_txt')
    while not button.is_displayed() :
        a = 10
    time.sleep(1)
    total = driver.find_element_by_xpath('//*[@id="conversion"]/div[2]/div[4]/button[1]')
    total.click() 
    
    root = tk.Tk()
    result = root.clipboard_get()
    print(result)
    some_list = result.splitlines()
    matching = [s for s in some_list if keyword in s]
    print(matching)
    mylist = []
    for x in matching :
    	mylist.append(some_list[some_list.index(x) + 2].split('-')[0])
    final_list = []
    for x in mylist:
        final_list.append(float(x[1:]))
    print(final_list)
    time.sleep(1)
    driver.quit()
    return final_list
    # return transcribe_urlip


#\convert_to_text("/home/priyanshu/Desktop/GTube/videoplayback.mp4", "you")
