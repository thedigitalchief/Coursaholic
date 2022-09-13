#!/usr/bin/env python3
''' USF Registration Script
This script is tied to the class monitoring script, and will be kicked off with
the available course request numbers. You must edit it to include your username
and password, it currently does not work perfectly, as the "Register" button on
OASIS is formatted weirdly, it cannot seem to "click" it
Copyright 2017 (c) Logan Lopez
'''

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def init_browser():
    browser = webdriver.Firefox()
    browser.wait = WebDriverWait(browser, 5)
    return browser

def register(crns):
    browser = init_browser()
    browser.get('https://my.usf.edu')
    try:
        username = browser.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password = browser.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        btn = browser.wait.until(EC.presence_of_element_located((By.ID, "btn-submit")))
        username.send_keys('rockydbull') # put in your username here
        password.send_keys('password') # put in your password here
        btn.click()
    except TimeoutException:
        print("blah") # it's honestly never timed out for me
    sleep(3)
    browser.get('https://bannersso.usf.edu/ssomanager/c/SSB')
    sleep(3)
    browser.get('https://usfonline.admin.usf.edu/pls/prod/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu')
    sleep(3)
    browser.get('https://usfonline.admin.usf.edu/pls/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu')
    sleep(3)
    browser.get('https://usfonline.admin.usf.edu/pls/prod/bwskfreg.P_AltPin')
    sem_sel = Select(browser.find_element_by_name('term_in'))
    sem_sel.select_by_visible_text("Spring 2019")
    sembtn = browser.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/form/input')))
    sembtn.submit()
    crnin = []
    sleep(3)
    for x in range(0,len(crns)):
       crnin.append(browser.wait.until(EC.presence_of_element_located((By.ID, "crn_id"+str(x+1)))))
    for x in range(0,len(crns)):
        crnin[x].send_keys(crns[x])
    regbtn = browser.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/form/input[19]")))
    regbtn.click() # this part doesn't work, but it will get you to the page with all the info filled in.
    # if you find a way to fix this please submit a pull request
