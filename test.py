import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import time
import streamlit as st

# A function to collect lego sets from search results on brickset.com
def collectLegoSets(startURL):
    time.sleep(4 + np.random.rand()*3)
    # Add headers to imitate a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    # Retrieve starting URL
    myPage = requests.get(startURL)

    # Parse the website with Beautiful Soup
    parsed = BeautifulSoup(myPage.text)

    # Grab all sets from the page
    a = [i for i in parsed.find_all('article')]

    # Create and empty data set
    newData = []

    # Iterate over all sets on the page
    for i in a:
        row = []
        # Add the set name to the row of data
        row.append(i.h1.text)
        try:
          price_s = i.find('dt', string='RRP').find_next_sibling().text
          price = float(re.search(r'(\u20AC)(\d+[.]\d{2})', price_s).groups()[1])
          row.append(price)
        except:
          row.append(np.nan)
        try:
         row.append(i.find('dt', string ='Pieces').find_next_sibling().text)
        except:
         row.append(0)
        try:
         row.append(i.find('dt', string ='Minifigs').find_next_sibling().text)
        except:
         row.append('')
        # Add the row of data to the dataset
        newData.append(row)
    newData = pd.DataFrame(newData, columns = ['Set', 'Price_Euro','Pieces','Minifigs'])

    # Check if there are more results on the "next" page
    try:
        nextPage = parsed.find('li', class_="next").a['href']
    except:
        nextPage = None

    # If there is another page of results, grab it and combine
    if nextPage:
        # Tell our program not to load new pages too fast by "sleeping" for two seconds before
        #   going to the next page
        time.sleep(2)
        # Merge current data with next page
        return pd.concat([newData, collectLegoSets(nextPage)], axis=0)
    # Otherwise return the current data
    else:
        return newData
    newData.to_csv("lego2019.csv", index=False)
    st.write(newData)
#st.dataframe(data)

data = collectLegoSets("https://brickset.com/sets/year-2019")
st.write("hello world")
