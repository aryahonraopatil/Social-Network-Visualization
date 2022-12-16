'''
Author: Salem Soin-Voshell
Filename: main.py
Description: Uses a hashtag and scrapes posts using it.
'''

#Selenium Imports
from multiprocessing import current_process
from operator import truediv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
import os
import wget
import time
import numpy as np
import pandas as pd

#Setting up data frame
data = {
    "account1": [],
    "location": [],
    "likes": [],
    "description": [],
    "time": []
}
accounts = pd.DataFrame(data)

#Settings & Passwords
HASHTAG = "travel"
username = "greydata76"
password = ""
account_wanted = 250

#Code:
#Opens window
driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.instagram.com")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#Logs in
SLusername = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
SLpassword = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
SLusername.clear()
SLpassword.clear()
SLusername.send_keys(username)
SLpassword.send_keys(password)
time.sleep(5)
SLlogin = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
time.sleep(10)

#Opens window with hashtag
driver.get("https://www.instagram.com/explore/tags/"+HASHTAG+"/")
post = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[role='link']"))).click()

#Add conditionals like try to some of these

#For loop that grabs x number of posts
current_count = 0
while current_count < account_wanted:
    #Gets post time
    try:
        SLtime = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "time[class='_aaqe']"))).get_attribute("datetime")
    except:
        SLtime = "_"
    print(SLtime)
    #Gets username
    try:
        SLusername = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _acan _acao _acat _acaw _a6hd']"))).get_attribute('innerText')
    except:
        SLusername = "_"
    print(SLusername)
    #Gets likes
    try:
        SLlikes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='_aacl _aaco _aacw _aacx _aada _aade']"))).get_attribute('innerText')
    except:
        SLlikes = "_"
    print(SLlikes)
    #Gets location
    try:
        SLlocation = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _aaqk _a6hd']"))).get_attribute('innerText')
    except:
        SLlocation = "_"
    print(SLlocation)
    #Gets description
    try:
        SLdescription = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='_aacl _aaco _aacu _aacx _aad7 _aade']"))).get_attribute('innerText')
    except:
        SLdescription = "_"
    print(SLdescription)
    current_count = current_count + 1
    #write current to pandas
    accounts.loc[len(accounts.index)] = [SLusername, SLlocation, SLlikes, SLdescription, SLtime]
    #click on next button
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Next']"))).click()
#Writes too csv
accounts.to_csv("export.csv")