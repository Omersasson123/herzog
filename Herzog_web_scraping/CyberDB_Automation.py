import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd 
from IPython.display import display
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
#import cchardet
import os
'''
Script to collect all relevant cybersecurity links
'''


#set up selenium
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito') #if we want to run selenium in incognito
#options.add_argument('--headless') #if we want to run selenium without displaying browser
driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)

#use driver to get webpage 
driver.get("https://www.cyberdb.co/database/cyberdb-cyber-vendors/")

#maximize window to ensure elements are where expected
driver.maximize_window()
'''
#scroll to bottom to avoid misclicking issue
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)
'''

#method to get all company urls that are relevant, as a set to make sure we don't have duplicates
list_of_startups = set()
def addToCompanyList(page_source):
    #create BeautifulSoup object
    soup = BeautifulSoup(page_source, 'lxml')
    result = soup.find('div', {"class": "all-request-data"})
    #find all links and only add them if they go to a company
    for link in result.findAll('a'):
        l = link.get('href')
        list_of_startups.add(l)
#scroll to bottom to avoid misclicking issue
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)
#check next_button exits //
next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='next page-numbers']")))
#next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div[7]/a[3]")))
#while next button exits collect links
while True:
    try:
        addToCompanyList(driver.page_source)
        print(len(list_of_startups))

        next_button.click()
        next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='next page-numbers']")))
    except:
        #have gone to last page
        break
    print(next_button)
print(len(list_of_startups))
driver.close()


'''
#ensure website locations are as expected, probably not needed
driver.maximize_window()
#click cyber_security tag, can letter edit to get companies of other tags 
time.sleep(2)
cyber_security = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='search-form']/div[2]/div/div/div[6]")))
cyber_security.click()

#scroll down to bottom of page and click load more button
time.sleep(3)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)
#click load more button
button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='companies_advanced_search_page']/div[4]/div")))
button.click()

#scroll to bottom
last_height = 0
while True:
    #scrolling
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    #check if we have reached end of scrolling
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

page_source = driver.page_source
#add all correct links to set of startups
addToCompanyList(page_source)
print(len(list_of_startups))
driver.close()


cyber_security_startup_table = pd.DataFrame()
for company in list_of_startups:
    df = add_rows(company, df)

path = os.getcwd()
df.to_csv(path + '/export_startup_companies.csv', index = False)
'''

