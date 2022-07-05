#For the regression model, we prepared a dataset consisting of:
#- Name_collection - Collection name;
#- N_elements - id of the collection element;
#- Rank - rank of the collection element;
#- Score - Item rarity score;
#- Items - Item traits;
#- Price - NFT price;
#- cClose - Ether price(only cryptopunks dataset).


import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import seaborn as sns
import plotly.express as px

#Uploading the file boredapeyachtclub
bored = pd.read_csv("boredapeyachtclub_for_graph.csv", sep = ',')
#Removing an extra column
bored = bored.drop(['Unnamed: 0'], axis=1)
#Uploading the file doodles-official
doodles = pd.read_csv("doodles-official_for_graph.csv", sep = ',')
#Removing an extra column
doodles = doodles.drop(['Unnamed: 0'], axis=1)
#Uploading the file cryptopunks
punks = pd.read_csv("cryptopunks_for_graph.csv", sep = ',')
#Removing an extra column
punks = punks.drop(['Unnamed: 0'], axis=1)
#Change column to date 
punks['date'] = pd.to_datetime(punks.date)

def correlation(df):
    #Correlation
    f, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(df.corr(), square=True, annot=True, cbar=True, ax=ax)

def price_punk(punks):
    #Top 5 Cryptopunk elements by number of sales
    punks_top =(punks[['date','N_elements', 'Price']])
    punks_top = punks_top[punks_top['N_elements'].isin([8970, 5575, 7072, 3914, 9117])]
    #Graph
    f, ax = plt.subplots(figsize=(15, 10))
    sns.lineplot(data=punks_top, x="date", y="Price", hue="N_elements", ax=ax,palette="bright",) 
    ax.set_title('Changing the price of Cryptopunk Elements', fontdict={'fontsize':16}, pad=12);

correlation(bored)

correlation(doodles)

correlation(punks)

price_punk(punks)



