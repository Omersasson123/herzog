import requests
from bs4 import BeautifulSoup
import pandas as pd 
from IPython.display import display


#use beautiful soup to extract data from first wiki table put first column as column names
page = requests.get("https://www.crowdstrike.com/services/")
soup = BeautifulSoup(page.content, 'html.parser')
#soup.find_all('p') returns list 
result = soup.findAll(text=True)
#cleaning text and printing it
clean = ""
blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',]
cleaned_text = ""
for item in result:
        if item.parent.name not in blacklist:
            cleaned_text += '{} '.format(item)
cleaned_text = cleaned_text.replace('\t', '')
cleaned_text = cleaned_text.replace('\n', ' ')
print(cleaned_text.strip())

