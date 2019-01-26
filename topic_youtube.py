# import dryscrape
# from bs4 import BeautifulSoup
# session = dryscrape.Session()
# myurl = "https://www.youtube.com/watch?v=5cQoGNEcc5Q"
# session.visit(my_url)
# response = session.body()
# soup = BeautifulSoup(response)
# soup.find(id="intro-text")
# # Result:
# <p id="intro-text">Yay! Supports javascript</p>

# from selenium import webdriver

# browser = webdriver.Chrome(executable_path='/home/ayushghd/Documents/imp/GTube/static/plugins/chromedriver.exe')

# browser.get("https://www.youtube.com/watch?v=5cQoGNEcc5Q")

# nav = browser.find_element_by_id("keyword")

# print(nav.text)

import requests
from bs4 import BeautifulSoup
url = "https://www.youtube.com/watch?v=5cQoGNEcc5Q"

web_r = requests.get(url)
web_soup = BeautifulSoup(web_r.text, 'html.parser')
print(web_soup.findAll('keywords'))