import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from opensea import OpenseaAPI
import requests
from opensea import utils as opensea_utils
import json
import time
import datetime
import os
import csv
from bs4 import BeautifulSoup
#================================================================================
#================================================================================
def rarity_scraping(collection_name):# Enter the name of the collection, as in OpenSea (for example web('azuki'), we take the name from https://opensea.io/collection/azuki).

    #NFT rank web scraping using BeautifulSoup from https://ranknft.io/

    #Create an empty Lists
    lst=[]

    #Insert the first page of the selected collection, should end with "?page=1"
    url = f'https://ranknft.io/collection/{collection_name}?page=1'
    params = {'page': 1}

    # set a number greater than the first page number to start the loop
    pages = 2
    n = 1

    while params['page'] <= pages:
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_='col-xl-spec15 col-md-2 col-sm-6 col-12 px-2 mb-4') #Collection element, class may change

        # name and rank scraping loop
        for n, i in enumerate(items, start=n):
            name = i.find('div', class_='mb-1').text.strip() #name NFT
            rank = i.find('div', class_='float-left pl-1').text # rank NFT
            lst.append([name,rank]) # add an element to the lists

        # Page navigation
        # [-2] penultimate value, because the last one is "Next"
        last_page_num = int(soup.find_all('a', class_='page-link')[-2].text) # class_='page-link' is the button "Next"
        pages = last_page_num if pages < last_page_num else pages
        params['page'] += 1

    # collection frame
    NFT_Rank = pd.DataFrame(lst)
    #In the rank column, leave only the number
    NFT_Rank[1] = NFT_Rank[1].str.split().str[0]
    #Save to csv file
    NFT_Rank.to_csv(f'{collection_name}.csv')
    return f'{collection_name}.csv'
