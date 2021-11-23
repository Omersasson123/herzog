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

#click USA comanies 
USA_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div[2]/ul/li[2]/a")))
USA_button.click()
time.sleep(2)
'''
#scroll to bottom to avoid misclicking issue
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)
'''

#method to get all company urls that are relevant, as a set to make sure we don't have duplicates
list_of_companies = set()
def addToCompanyList(page_source):
    #create BeautifulSoup object
    soup = BeautifulSoup(page_source, 'lxml')
    result = soup.find('div', {"class": "all-request-data"})
    #find all links and only add them if they go to a company
    for link in result.findAll('a'):
        l = link.get('href')
        list_of_companies.add(l)
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
        print(len(list_of_companies))

        next_button.click()
        next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='next page-numbers']")))
    except:
        #have gone to last page
        break
    print(next_button)
print(len(list_of_companies))
driver.close()

#sonya's webscraping code
def clean_data(df):
    # removes the \n characters 
    df = df.replace(r'\$M ',' ', regex=True) 
    return df

def add_rows(url, df):
    #request page and initilze BS object
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find('body')
    
    result = soup.find('div', {"class": "zyno-card-4"})
    titles = [ ]
    values = [ ]

    
    
    name_of_company = body.find("h1", {"class": "uk-article-title"}).text
    titles.append('Name of Company')
    values.append(name_of_company)
    
    
    arr = [ ]

    first_col = body.find_all("div", {"class": "col-width-oneth"})
    title_indeces = [2, 5, 8, 11, 14]
    value_indeces = [3, 6, 9, 12, 15]
    for i in first_col:
        arr.append(i.text)
    
    for index in title_indeces:
        titles.append(arr[index])
    for index in value_indeces:
        values.append(arr[index])
        
    arr_of_tags = []
    tag_wrap = body.find("div", {"class": "vendor-categories-th-p"}).find_all('a')
    for i in tag_wrap:
        arr_of_tags.append(i.text)
    
    
    location = body.find("div", {"class": "vendor-country"}).text
    #the about description
    about_vendor = body.find("div", {"class": "vendor-description"}).text
    
    titles.extend(['Company Tags', 'Location', 'Description'])
    values.extend([arr_of_tags, location, about_vendor])
    
    

    row_df = pd.DataFrame([values], columns = titles)
  
    df = pd.concat([df, row_df], ignore_index=True)
    
    #df = df.drop_duplicates() #ensure we don't add duplicates, should add company name to avoid drops of same values 
    df = clean_data(df)
    return df


cyber_security_multinational_table = pd.DataFrame()
l = list(list_of_companies)
for company in l:
    time.sleep(2)
    print(company)
    cyber_security_multinational_table = add_rows(company, cyber_security_multinational_table)

path = os.getcwd()
cyber_security_multinational_table.to_csv(path + '/export_multinational_companies.csv', index = False)


