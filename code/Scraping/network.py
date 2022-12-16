'''
Author: Salem Soin-Voshell
Filename: network.py
Description: 
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

#Makes queue of tuples, first is name second is depth.
queue = [("lanita_dinamita", 0)]

#Settings
#Following atleast x accounts
min_following = 0
#Following at max x accounts
max_following = 500
#Location within x days
days_limit = 21
#Account limit
acc_limt = 10000
#Depth Limt
depth_limit = 4
#First x - Only get x number of following when scraping
first_following = 10

#Get current date.

#Login Info
username = "iganalysis22"
password = ""

#Setting up data frame
data = {
    "name": [],
    "tag": [],
    "follower_count": [],
    "following_count": [],
    "following_list": [],
    "post_count": [],
    "location": [],
    "long": [],
    "lat": [],
    "bio": [],
    "depth": []
}
accounts = pd.DataFrame(data)

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
time.sleep(5)

#Get Account Function
#If account doesn't match requirements function returns tuple of False
#otherwise returns tuple with info.
def get_account(account_tup, curr_driver):
    curr_driver.get("https://www.instagram.com/"+account_tup[0]+"/")
    #Get Post Count    
    try:
        post_count = WebDriverWait(curr_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='_ac2a']"))).get_attribute('innerText')
        print("Post Count:")
        print(post_count)
    except:
        post_count = 0

    #Gets following count
    gen_data = driver.find_elements(By.CSS_SELECTOR, "span[class='_ac2a']")
    print("Following")
    following_count = gen_data[2].get_attribute("innerText")
    print(following_count) #Following
    try:
        following_int = int(gen_data[2].get_attribute("innerText"))
        if((following_int >= min_following and following_int <= max_following) == False):
            return (False)
    except:
        return (False)

    #Gets followers count
    follower_count = gen_data[1].get_attribute("innerText")
    print("Followers")
    print(follower_count) #Followers

    #Get Bio
    bio_data = driver.find_element(By.CSS_SELECTOR, "div[class='_aa_c']")
    username = bio_data.find_element(By.CSS_SELECTOR, "span[class='_aacl _aacp _aacw _aacx _aad7 _aade']").get_attribute("innerText")
    try:
        bio = bio_data.find_element(By.CSS_SELECTOR, "div[class='_aacl _aacp _aacu _aacx _aad6 _aade']").get_attribute("innerText")
    except:
        bio = "na"
    try:
        bio_link = bio_data.find_element(By.CSS_SELECTOR, "div[class='_aacl _aacp _aacw _aacz _aada _aade']").get_attribute("innerText")
    except:
        bio_link = "na"
    print("Username:")
    print(username)    
    print("Bio:")
    print(bio)
    print("Bio Link:")
    print(bio_link)
    #Looks at latest posts
    #If time is out of range return false
    #If location is missing continue, otherwise use location
    sentinel = True
    post = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='_aagu']"))).click()
    while sentinel:
        try:
            time = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "time[class='_aaqe']"))).get_attribute("datetime")
            print(time)
        except:
            time = "-"
        #If Time is in range:
        if True:
            try:
                location = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _aaqk _a6hd']"))).get_attribute('innerText')
            except:
                location = "_"
            print(location)
            if location != "_":
                try:
                    geolocator = Nominatim(user_agent="my_user_agent") 
                    loc = geolocator.geocode(location)
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
                print(long)
                print(lat)
        else:
            #If time isn't in range we are done.
            return (false)
        if(lat != "_" and long != "_"):
            #If in range and location valid, move on.
            print("Sentinel Set to False")
            sentinel = False
        #Try and click next otherwise return false
        if(sentinel == True):
            try:
                next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg[aria-label='Next']"))).click()
            except:
                return (False)
    #Need to click the little x.
    driver.find_element(By.CSS_SELECTOR, "div[class='x78zum5 x6s0dn4 xl56j7k xdt5ytf']").click()
    #time.sleep(10)
    print("Exited Loop")
    #Get following list
    #time.sleep(10)
    #driver.get("https://www.instagram.com/"+account_tup[0]+"/")
    #time.sleep(3)
    #print("Post sleep and reload")
    maxfollowers = following_int
    gen_data = driver.find_elements(By.CSS_SELECTOR, "span[class='_ac2a']")
    followers_link = gen_data[2]
    followers_link.click()

    ##DELETE LATER
    maxfollowers = 6
    #driver.implicitly_wait(30)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='_aacl _aacp _aacw _aacz _aad6 _aadb']")))
        followers_list = driver.find_elements(By.CSS_SELECTOR, "div[class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9o _abcm']")[1]
    except:
        print("BRUH!")
    number_of_followers_in_list = len(followers_list.find_elements(By.CSS_SELECTOR, "div[class=' _ab8y  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm']"))
    action_chain = webdriver.ActionChains(driver)
    action_chain.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    action_chain.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    action_chain.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    action_chain.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    action_chain.key_down(Keys.TAB).key_up(Keys.TAB).perform()
    while number_of_followers_in_list < maxfollowers:
        action_chain.key_down(Keys.DOWN).perform()
        number_of_followers_in_list = len(followers_list.find_elements(By.CSS_SELECTOR, "div[class=' _ab8y  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm']"))
    action_chain.key_up(Keys.DOWN).perform()
    #Collect info from html elements
    followers = []
    for user in followers_list.find_elements(By.CSS_SELECTOR, "div[class=' _ab8y  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm']"):
        followers.append(user.get_attribute("innerText"))
    return 

try:
    get_account(queue[0], driver)
except:
    print("Private Account or Error")

#While both are in range, depth etc
#pop top account
#check popped account isn't in pandas
#if it is skip too next person
#Write pandas and export csv every time.