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
def dataframe_cleaning_rankings(rarity_ranking_csv):

    df = pd.read_csv(rarity_ranking_csv)

    #checking if 'Unnamed' column exists, if yes, dropping it from the df
    if ('Unnamed: 0') in df.columns.tolist():
        df.drop(['Unnamed: 0'], axis=1, inplace=True)

    #renaming columns
    df.rename(columns={'0': "ID", '1': "rarity"}, inplace=True)

    #removing useless characters
    df['ID'].replace(regex=True, inplace=True, to_replace=r'\D', value=r'')

    #converting strings to integers
    df['ID'] = df['ID'].astype(int)

    return df
