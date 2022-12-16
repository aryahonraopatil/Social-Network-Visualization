'''
Author: Salem Soin-Voshell
Filename: profile.py
Description: Uses a list of instagram accounts and cycles through them, downloading x number of their latest posts, 
and information related to posts. If posts are geotagged, it will attempt to translate that to long, lat. 
All information is stored in pandas dataframes and exported to a csv after every account is scraped.
'''

#Selenium Imports
from ast import Slice
from multiprocessing import current_process
from operator import truediv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait 
from geopy.geocoders import Nominatim
import os
import wget
import time
import numpy as np
import pandas as pd


#Setting up data frame
data = {
    "account1": [],
    "followers": [],
    "post_count": [],
    "post_link": [],
    "location": [],
    "long": [],
    "lat": [],
    "likes": [],
    "description": [],
    "time": []
}
accounts = pd.DataFrame(data)

#Settings & Login Information 
HASHTAG = "travel"
username = "greydata76"
password = ""
account_wanted = 50

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

#Reads in list of accounts to scrape.
scrape_list = pd.read_csv("export.csv")
name_list = scrape_list['account1'].tolist()
loc_list = scrape_list['location'].tolist()

#Sets starting location, can be used if previous scrape got interupted.
location_in_list = 0

#While loop that keeps track of profile scraper is on.
while location_in_list < len(name_list):
    #If account did not use geotags, don't scrape it.
    if(loc_list[location_in_list] == "_"):
        location_in_list = location_in_list + 1
    else:
        driver.get("https://www.instagram.com/"+name_list[location_in_list]+"/")
        #Scrapes followers
        try:
            SL_followers = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='_ac2a']"))).get_attribute('innerText')
            print(SL_followers)
        except:
            SL_followers = 0
        #Converts followers to int,
        try:
            NEW_followers = int(SL_followers)
        except:
            NEW_followers = 100
        #Only continues to scrape profile if they have over 99 followers.
        if(NEW_followers > 99):
            #Opens first post on page.
            post = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='_aagu']"))).click()
            current_count = 0
            #Loops through posts until count wanted is hit or all of the posts are scraped.
            while current_count < account_wanted:
                #Gets time of post
                try:
                    SLtime = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "time[class='_aaqe']"))).get_attribute("datetime")
                except:
                    SLtime = "_"
                print(SLtime)
                #Gets username of poster.
                try:
                    SLusername = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _acan _acao _acat _acaw _a6hd']"))).get_attribute('innerText')
                except:
                    SLusername = "_"
                print(SLusername)
                #Gets likes on post
                try:
                    SLlikes = driver.find_elements(By.CSS_SELECTOR, "div[class='_aacl _aaco _aacw _aacx _aada _aade']")
                    SLlikes = SLlikes[len(SLlikes)-1].get_attribute('innerText')
                except:
                    SLlikes = "_"
                print("Likes:" + SLlikes)
                #Gets location, if it was given.
                try:
                    SLlocation = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _aaqk _a6hd']"))).get_attribute('innerText')
                except:
                    SLlocation = "_"
                print(SLlocation)
                #Gets Description
                try:
                    SLdescription = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='_aacl _aaco _aacu _aacx _aad7 _aade']"))).get_attribute('innerText')
                except:
                    SLdescription = "_"
                print(SLdescription)
                #Attempts to translate geotag to long/lat
                try:
                    geolocator = Nominatim(user_agent="my_user_agent") 
                    loc = geolocator.geocode(SLlocation)
                    try:
                        long = loc.longitude
                    except:
                        long = "_"
                    try:
                        lat = loc.latitude    
                    except:
                        lat = "_"
                except:
                    lat = "_"
                    long = "_"
                post_count = 10
                post_link = "_"
                current_count = current_count + 1
                #write current to pandas
                accounts.loc[len(accounts.index)] = [SLusername, SL_followers, post_count, post_link, SLlocation, long, lat, SLlikes, SLdescription, SLtime]
                #click on next button
                try:
                    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Next']"))).click()
                except:
                    current_count = account_wanted
        #Saves dataframe to csv
        accounts.to_csv("profiles/export.csv")
        #To export json try something like
        accounts.to_json("profiles/export.json", orient='records')
        location_in_list = location_in_list + 1