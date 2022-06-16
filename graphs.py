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

def graphs(df, collection_name):

    fig, ax = plt.subplots()

    plt.scatter(df['Price'], df['rarity'], s=15, alpha=0.8)
    plt.xlabel('Price ($)')
    plt.ylabel('Rarity')
    plt.title(f'Rarity v Price ({collection_name} collection)')

    plt.savefig(f'{collection_name}_Rarity v Price.png')

    plt.show()
