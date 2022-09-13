#!/usr/bin/env python3
''' USF Class Monitor
This script monitors provided Course Request Numbers for classes available at
the University of South Florida (all campuses), and then if it detects an 
opening in the class it will attempt to register you through the selenium script
called usf_reg.py. You can easily modify it to email you, however there exists
another project which hooks in with Twilio to text the student
https://github.com/luqmaan/USFClassNodeifier
Copyright 2019 (c) Logan Lopez
'''
import requests
import logging
from bs4 import BeautifulSoup
import usf_reg

logging.basicConfig(level=logging.INFO, format='%(levelname)-6s %(message)s')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

def check_diff(url, crns):
    opened = []
    session = requests.session()
    for crn in crns: # change P_SEMESTER to match the semester your searching for classes
        data = {"P_SEMESTER": "202108","P_SESSION": "","P_CAMPUS": "","P_DIST": "","P_COL": "","P_DEPT": "","p_status": "", "p_ssts_code": "","P_CRSE_LEVL": "","P_REF": crn,"P_SUBJ": "","P_NUM": "","P_TITLE": "","P_CR": "","p_day_x": "no_val","p_day": "no_val", "P_TIME1": "","P_INSTRUCTOR": "","P_UGR": ""}
        site = session.post(url, headers=headers, data=data)
        soup = BeautifulSoup(site.content, "lxml")
        course = soup.table
        courseTable = course.table
        rows = courseTable.find_all('td')
        results = [i.text for i in rows]
        if results[10] == "Closed":
            logging.debug("Class unavailable: "+ results[7])
        else:
            opened.append(crn)
            logging.debug("Class available: " + results[7])
    if len(opened) > 0:
        logging.debug("Classes ready to submit")
        usf_reg.register(opened)

check_diff('https://usfweb.usf.edu/DSS/StaffScheduleSearch/StaffSearch/Results', ["12345", "23456", "34567"]) # Input the CRNs of interest here
