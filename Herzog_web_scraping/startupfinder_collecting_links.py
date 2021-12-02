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
from webdriver_manager.chrome import ChromeDriverManager
import os
'''
Script to collect all relevant cybersecurity links
'''


#set up selenium
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito') #if we want to run selenium in incognito
options.add_argument('--headless') #if we want to run selenium without displaying browser
#driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())

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
#//*[@class='label hoverable js-suggested-tag js-hoverable-tag js-binded tooltipstered']
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

#Sonya's Code
def clean_data(df):
    # removes the \n characters 
    df = df.replace(r'\n',' ', regex=True) 
    return df
    
def add_tags(soup):
    #returns an array of tags from the soup
    arr_of_tags = []
    tag_wrap = soup.findAll('div', class_ = 'tags-wrapper')[0]
    for i in tag_wrap.find_all('div', {"class":'label hoverable js-hoverable-tag'}):
        tag = i.find('a', {"data-report-action": "TAGS"}).find(text=True)
        arr_of_tags = np.append(arr_of_tags, tag)
    return arr_of_tags   

df = pd.DataFrame()
def add_rows(url, df):
    #request page and initilze BS object
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    #find box
    result = soup.find('div', {"class": "zyno-card-4"})
    column = []
    value = []
    
    # add name of company 
    column.append('Company Name')
    title = soup.find('div', {"class": "breadcrumb-item breadcrumb-item-bolded"}).find(text=True)
    value.append(title)
    
    #extract info (column and values)
    for metadata_item in result.findAll('div', {"class": 'metadata-item'}):
            value_for_col = metadata_item.find('div', {"class":'metadata-description'})
            col_name = metadata_item.find('div', {'class': 'item-bottom'})
            if col_name and value_for_col:
                column.append(col_name.find(text=True))
                value.append(value_for_col.findAll(text=True)[0]) #for some reason takes it as a list
    
    funding = soup.findAll('div', {"class": 'funding-metadata'})
    if funding != None and len(funding) > 0:
        funding = funding[0]
        for i in range(4):
                value_for_col = funding.findAll("div", {"class": "title"})[i]
                col_name = funding.findAll("div", {"class": "subtitle"})[i]
                if col_name and value_for_col:
                    column.append(col_name.find(text=True))
                    value.append(value_for_col.findAll(text=True)[0]) #for some reason takes it as a list    
    present_fund = soup.find('div', {"class": 'funding-round-events-wrapper'})
    if present_fund != None:
        name_of_round = present_fund.find('div', {"class": 'text medium bold'}) #.find(text=True)
        amount = present_fund.find('div', {"class": 'text bold big text-align-end'}) #.find(text=True)
        if name_of_round:
            column.append('Current Round')
            value.append(name_of_round.find(text = True))
        if amount:
            column.append('Funding in Current Round')
            value.append(amount.find(text = True))
    #add tags to the values 
    arr_of_tags = add_tags(soup)
    column.append('TAGS')
    value.append(arr_of_tags)
    
    #create new_df with new row and add that to existing dataframe
    row_df = pd.DataFrame([value], columns = column)
  
    df = pd.concat([df, row_df], ignore_index=True)
    
    #df = df.drop_duplicates() #ensure we don't add duplicates, should add company name to avoid drops of same values 
    
    #clean data 
    df = clean_data(df)
    return df
 

cyber_security_startup_table = pd.DataFrame()
for company in list_of_startups:
    df = add_rows(company, df)

path = os.getcwd()
df.to_csv(path + '/export_startup_companies.csv', index = False)


