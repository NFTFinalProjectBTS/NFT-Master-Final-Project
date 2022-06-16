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
import  yfinance  as  yf
#================================================================================
#================================================================================

def dataframe_cleaning_collection(collection_csv):

    df = pd.read_csv(collection_csv)

    #checking if 'Unnamed: 0' column exists, if yes, dropping it from the df
    if ('Unnamed: 0') in df.columns.tolist():
        df.drop(['Unnamed: 0'], axis=1, inplace=True)

    #conversion rates from Yahoo finance, getting the lastest Close price available
    eth_dol = yf.download('ETH-USD')['Close'][-1]
    weth_dol = yf.download('WETH-USD')['Close'][-1]
    ape_dol = yf.download('APE3-USD')['Close'][-1]

    #finding in the df all the values that corresponds to the 3 uniques currency symbols
    price_eth =  df['Symbol'] == 'ETH'
    price_weth =  df['Symbol'] == 'WETH'
    price_ape =  df['Symbol'] == 'APE'

    df.loc[price_eth, 'Price'] = df.loc[price_eth, 'Price'] * eth_dol
    df.loc[price_weth, 'Price'] = df.loc[price_weth, 'Price'] * weth_dol
    df.loc[price_ape, 'Price'] = df.loc[price_ape, 'Price'] * ape_dol

    # Unify Symbol column by changing corresponding values to 'dollar'
    df.loc[price_eth, 'Symbol'] = 'dollar'
    df.loc[price_weth, 'Symbol'] = 'dollar'
    df.loc[price_ape, 'Symbol'] = 'dollar'

    # Assert that only dollar currency remains
    assert df['Symbol'].unique() == 'dollar'

    return df, eth_dol
