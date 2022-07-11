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

from sklearn.cluster import AgglomerativeClustering
#================================================================================
#================================================================================
def clustering(df, collection_name):

    X = df[['Price','rarity']]
    X = np.array(X)

    linkages = ['single', 'average', 'complete', 'ward']

    for linkage in linkages:

        clustering = AgglomerativeClustering(n_clusters=5, linkage=linkage).fit(X)

        labels = clustering.labels_

        plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')

        plt.title(f'Linkage = {linkage}')

        #plt.show()

    #perform a second time clustering with the best linkage: average
    AC = AgglomerativeClustering(n_clusters=5, linkage='average').fit(X)
    AC_labels = AC.labels_

    #create new column with the labels for each cluster group
    df['Labels'] = AC_labels

    #create a list of cluster
    df_cluster = df[df['Labels'] == 4]
    nft_under_priced = df_cluster.index.sort_values().tolist()

    #creating a dataframe displaying the list created above
    df_sniped = df_cluster.reset_index('ID')[['ID']].sort_values(by='ID').reset_index().drop(['index'], axis=1)
    df_sniped.to_csv(f'{collection_name}_sniped.csv')

    #put the labels in a list to use it for the legend of the plot
    labels_k = []
    for i in np.unique(AC_labels):
        n = np.unique(AC_labels)[i]
        labels_k.append(n)

    fig, ax = plt.subplots()

    #plot lines in the center of the axes to get the buy/sell/hold threshold
    scatter = plt.scatter(X[:, 0], X[:, 1], c=AC_labels, cmap='viridis')

    plt.xlabel('Price ($)')
    plt.ylabel('Rarity')
    plt.title(f'{collection_name} collection\nLinkage = Average')
    #plt.axvline(x=(X[:,0].max() - X[:,0].min()) / 2, color='black', linestyle='--')
    #plt.axhline(y=(X[:,1].max() - X[:,1].min()) / 2, color='black', linestyle='--')

    #plotting text boxes
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    #looping for the 4 text boxes
    ax.text(0.025, 0.075, 'Buy', transform=ax.transAxes, fontsize=16, verticalalignment='top', bbox=props)

    plt.legend(handles=scatter.legend_elements()[0], labels=labels_k)

    plt.savefig(f'{collection_name}_clustering.png')

    plt.show()

    return df_cluster, df_sniped, fig
