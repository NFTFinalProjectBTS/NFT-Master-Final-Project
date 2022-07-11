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
from PIL import Image
#================================================================================
#================================================================================
# Read secret API file to retrieve the key and create an object to interact with the Opensea API

slugs = ['doodles-official', 'boredapeyachtclub']

def collection_info(collection_slug):

    Key = pd.read_csv('NiFTy1API.csv')
    OPENSEA_APIKEY = str(Key.columns[0])
    api = OpenseaAPI(apikey = OPENSEA_APIKEY)

    result = api.collection(collection_slug = collection_slug)

    collection = result["collection"]
    stats = collection["stats"]
    traits = collection["traits"]
    #fetching the floor price for said collection
    floor_price = float(stats['floor_price'])

    collection_image = collection['image_url']

    collection_description = collection['description']

    items = int(stats['count'])
    owners = stats['num_owners']
    floor_price = stats['floor_price']
    total_volume = str(round((int(stats['total_volume']) / 1000), 1)) + 'k'

    return floor_price, collection_image, collection_description, items, owners, floor_price, total_volume
