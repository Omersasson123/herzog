import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd 
from IPython.display import display
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
driver.get("https://finder.startupnationcentral.org/startups/search?tab=all&list_1_action=and&list_2_action=and&list_3_action=and&list_4_action=and&list_5_action=and&list_6_action=and&list_7_action=and&list_8_action=and&list_9_action=and&list_10_action=and&list_11_action=and&list_12_action=and&list_13_action=and&list_14_action=and&list_15_action=and&list_16_action=and&list_17_action=and&list_18_action=and&list_19_action=and&list_20_action=and&founded_from_year=&founded_to_year=&status=Active&academia_based=0&time_range_code=2&time_range_from_date=2021-09-19")

#maximize window to ensure elements are where expected
driver.maximize_window()
#scroll to bottom to avoid misclicking issue
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)
#start login process
button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='side-navbar-wrapper']/div/div[2]/div/div[2]/div/div")))
button.click()
time.sleep(3)
#move past popup to gmail sign in
login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='login-agree']")))
login.click()
time.sleep(3)
google = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div/div[2]/div[2]/div/div/div[1]/div[5]")))
google.click()
time.sleep(3)
#put in gmail and password
email_login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='identifierId']")))
email_login.send_keys("herzhog12@gmail.com")
time.sleep(1)
next1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='identifierNext']/div/button")))
next1.click()

time.sleep(3)
password_login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")))
password_login.send_keys("tamidherzhog12")
time.sleep(1)
next1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='passwordNext']/div/button")))
next1.click()
time.sleep(10)

#method to get all company urls that are relevant, as a set to make sure we don't have duplicates
list_of_startups = set()
def addToCompanyList(page_source):
    #create BeautifulSoup object
    soup = BeautifulSoup(page_source, 'lxml')
    result = soup.find('div', {"class": "js-company-cards-list js-search-items-list company-cards-list"})
    #find all links and only add them if they go to a company
    for link in result.findAll('a'):
        l = link.get('href')
        if 'company_page' in l:
            list_of_startups.add('https://finder.startupnationcentral.org' + l)

#ensure website locations are as expected, probably not needed
driver.maximize_window()
#click cyber_security tag, can letter edit to get companies of other tags 
time.sleep(2)
cyber_security = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='search-form']/div[2]/div/div/div[6]")))
cyber_security.click()

#scroll down to bottom of page and click load more button
time.sleep(5)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(5)
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
print(list_of_startups)
driver.close()

