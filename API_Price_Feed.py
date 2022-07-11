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
#================================================================================
#================================================================================

# Read secret API file to retrieve the key and create an object to interact with the Opensea API
Key = pd.read_csv('NiFTy1API.csv')
OPENSEA_APIKEY = str(Key.columns[0])
api = OpenseaAPI(apikey = OPENSEA_APIKEY)

#=============================================================================================================
#=============================================================================================================
#WORK IN PROGRESS
#goal is to have a list of all targeted collections stored in a csv and run the API for this list
#dfCollections = pd.read_csv('CollectionSmartContractAddress.csv') #csv and Smart Contract list in progress
#=============================================================================================================
#=============================================================================================================


#set Collection and smart_contract_address
Collection = 'Doodles'
smart_contract_address = '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e'

#start loop to retrieve the listed price
ListingPrice = []
RangeList = [i for i in range (9999)] #if i != 318 for example if single NFTs are not included on OpenSea

#connect to the API and create loop
for i in RangeList:
    import requests
    url = f"https://api.opensea.io/api/v1/asset/{smart_contract_address}/{i}/listings?limit=1"
    headers = {
    "Accept": "application/json",
    "X-API-KEY": f'{OPENSEA_APIKEY}'
    }

    response = requests.get(url, headers=headers)

    if response.text != '{"listings":[]}' and '{"message":"failure to get a peer from the ring-balancer"}':
        currenttextprice = json.loads(response.text)['listings'][0]['current_price']
        #text price has to be cleaned by '10**18'
        currentprice = float(currenttextprice)/10**18
        ListedCoin = json.loads(response.text)['listings'][0]['payment_token_contract']['symbol']


    #during the Loop print ID and Price of the retrieved listed Data - helps to check if it fails to check
        print(json.loads(response.text)['listings'][0]['metadata']['asset']['id']), print('Price', currentprice, ListedCoin)

        time.sleep(0.001)

        ListingPrice.append((i,currentprice, ListedCoin))

    #create DataFrame
df = pd.DataFrame(ListingPrice, columns = ['ID', 'Price', 'Symbol']).set_index('ID')
df.to_csv(f'{Collection} Price.csv')
