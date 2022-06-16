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

def outlier_analysis(df, floor_price):

    #ensuring that all data collected is equal of above the floor price
    df1 = df[df['Price'] >= floor_price]

    Q1 = df1['Price'].quantile(0.25)
    Q3 = df1['Price'].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5*IQR
    lim_sup = Q3 + 1.5*IQR

    count = 0
    outliers = []

    #looping through the price column to count the number of outliers and put them in a list
    for i in df1['Price']:
        if (i < lim_inf) or (i > lim_sup):
            count += 1
            outliers.append(i)
    #print("The total number of outliers is:",count)

    for i in df1['Price']:
        #calculating the median for each array
        variable_median = df['Price'].median()

        #replacing the outliers by the median
        df1['Price'] = df1.loc[:, 'Price'].apply(lambda x:variable_median if x > lim_sup or x < lim_inf else x)

    return df1
