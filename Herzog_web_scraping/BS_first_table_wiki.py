import requests
from bs4 import BeautifulSoup
import pandas as pd 
from IPython.display import display

#use beautiful soup to extract data from first wiki table put first column as column names
page = requests.get("https://en.m.wikipedia.org/wiki/CrowdStrike")
soup = BeautifulSoup(page.content, 'html.parser')
#soup.find_all('p') returns list 
result = soup.find('table')
column = []
value = []
for row in result.findAll('tr'):
        col = row.find('th')
        val = row.find('td')
        if col and val:
                print(val.findAll(text = True))
                column.append(col.find(text=True))
                value.append(val.findAll(text=True))

#creating data frame
df = pd.DataFrame([value[0]], columns = [column[0]])
for i in range(1, len(column)):
        df[column[i]] = [value[i]]

#Only use pandas but doesn't save what as column names? 
import pandas as pd
url = "https://en.m.wikipedia.org/wiki/CrowdStrike"
tables = pd.read_html(url) 
#print(tables[0]) #to print first table