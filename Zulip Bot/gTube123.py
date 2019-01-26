
# Zulip Bot by Team Ganador

import datetime
import os
import zulip
import os
import time
import requests 
import tkinter as tk
from selenium import webdriver
from sys import platform
import urllib.request
from xml.etree import ElementTree
from selenium.webdriver.support.wait import WebDriverWait

proxy = 'http://edcguest:edcguest@172.31.100.14:3128'
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#BASE_DIR = os.path.dirname("/home/aayushshivam7/")
DRIVER_NAME = "chromedriver.exe" if platform == "win32" else "chromedriver"
DRIVER_DIR = os.path.join(BASE_DIR, "plugins", DRIVER_NAME)

chatbotPage = "file:///home/shreyas/Desktop/Hack36/index.html"
duration = '00:00:05'

def wait_for_page_load(driver, timeout=30):
        old_page = driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(driver, timeout).until(
            staleness_of(old_page)
        )

def queryBot(inMsg) :

    terminateWord = ["stop" , "terminate" , "exit" , "end"]

    if inMsg in terminateWord : 
        return False

    txtInput.send_keys(inMsg)
    txtInput.send_keys(u'\ue007')

    time.sleep(2)

    txtOutput = driver.find_element_by_id("result").text
    txtOutput = ([i for i in txtOutput.split('\n') if i][-1])
    
    return (txtOutput)  




class gTube123(object):

    def usage(self):
        return "Hi I am GTubeBot !!! "
    
    def handle_message(self, message, bot_handler) :
        
        client = zulip.Client(config_file="/usr/local/lib/python3.5/dist-packages/zulip_bots/bots/gTube123/zuliprc")
        request = {
            "type": "private",
            "to": "GTube1234-bot@hack36.zulipchat.com",
            "content": message
        }
        result = client.send_message(request)


    def handle_message2(self, message, bot_handler):

        videoSearchIntent = ["Tell me the title of your video", "Okay, tell me what to search for", "Tell me the name of the video", "What do you want me to search"]
        summarizeVideoIntent = ["Summarizing video for you", "Summarizing ...", "Creating summary for you"]
        searchWordIntent = ["Tell me what to search for in the video", "Okay, tell me what to search for in this", "What do you want me to search in this"]
        detectObjectIntent = ["Tell me what object to search for in the video", "Okay, tell me the object which is to be searched", "What object do you want me to search in this"]

        global state
        global videoSearchFlag
        global summarizeVideoFlag
        global searchWordFlag
        global detectObjectFlag

        client = zulip.Client(config_file="/usr/local/lib/python3.5/dist-packages/zulip_bots/bots/gTube123/zuliprc")
        inMsg = message['content']

        if state :
            outMsg = queryBot(inMsg)
        elif videoSearchFlag :
            outMsg = "Searching for "+inMsg+" ..."
        elif summarizeVideoFlag :
            temp=0
        elif searchWordFlag :
            outMsg = "Searching for "+inMsg+" in the video ..."
        elif detectObjectFlag :
            outMsg = "Searching for "+inMsg+" in this video ..."

        txtOutput = outMsg

        videoSearchFlag = txtOutput in videoSearchIntent
        # summarizeVideoFlag = txtOutput in summarizeVideoIntent
        searchWordFlag = txtOutput in searchWordIntent
        detectObjectFlag = txtOutput in detectObjectIntent
        state = True ^ (videoSearchFlag | summarizeVideoFlag | searchWordFlag | detectObjectFlag)

        print (outMsg)

        return outMsg


driver = webdriver.Chrome(DRIVER_DIR)
driver.get(chatbotPage)
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
txtInput = driver.find_element_by_xpath("//*[@id='query']")

state = True
videoSearchFlag = False
summarizeVideoFlag = False
searchWordFlag = False
detectObjectFlag = False

handler_class = gTube123

