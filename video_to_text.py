import os
import requests 
from selenium import webdriver
from sys import platform
from xml.etree import ElementTree

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#BASE_DIR = os.path.dirname("/home/aayushshivam7/")
DRIVER_NAME = "chromedriver.exe" if platform == "win32" else "chromedriver"
DRIVER_DIR = os.path.join(BASE_DIR, "plugins", DRIVER_NAME)
converter = "https://www.360converter.com/conversion/video2TextConversion?type=v2t"
duration = '00:00:30'
#JS_SCRIPT = 'if(yt.config_.TTS_URL.length) window.location.href=yt.config_.TTS_URL+"&kind=asr&fmt=srv1&lang=en"'
# JS_SCRIPT = 'if(yt.config_.TTS_URL != "") window.location.href=yt.config_.TTS_URL+"&kind=asr&fmt=srv1&lang=en"'

def convert_to_text(filePath):

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

    submit = driver.find_element_by_id('StartConvert')
    submit.click()

    
    sleep(10)
    driver.quit()
    # return transcribe_urlip


convert_to_text("/home/aayushshivam7/Desktop/Hack36/Yoogle/videoplayback.mp4")
