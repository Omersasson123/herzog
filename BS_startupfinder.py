import requests
from bs4 import BeautifulSoup
import pandas as pd 
from IPython.display import display

df = pd.DataFrame()
def add_rows(url, df):
    #request page and initilze BS object
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #find box
    result = soup.find('div', {"class": "zyno-card-4"})
    column = []
    value = []
    #extract info (column and values)
    for row in result.findAll('div', {"class": 'metadata-item'}):
            col = row.find('div', {"class":'metadata-description'})
            val = row.find('div', {'class': 'item-bottom'})
            if col and val:
                column.append(col.find(text=True))
                value.append(val.findAll(text=True)[0]) #for some reason takes it as a list
    #create new_df with new row and add that to existing dataframe
    row_df = pd.DataFrame([column], columns = value)
    df = pd.concat([df, row_df])
    df = df.drop_duplicates() #ensure we don't add duplicates, should add company name to avoid drops of same values 
    return df
df = add_rows("https://finder.startupnationcentral.org/company_page/snyk", df)
df = add_rows("https://finder.startupnationcentral.org/company_page/orca-security", df)
print(df)
