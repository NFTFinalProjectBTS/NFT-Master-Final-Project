from Main import *
from sell import *
from clustering import *
from API_collection_info import *
############################################################################
############################################################################
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
############################################################################
############################################################################
############################################################################
def sell_function(full_collection_csv, rarity_ranking_csv, collection_name, collection_slug):
    st.write('Provide an NFT ID and it will predict a price based on its rarity compared to similar rarities in the collection')
    df_rarity = dataframe_cleaning_rankings(rarity_ranking_csv)
    df = NFT_analysis(collection_name, collection_slug, full_collection_csv, rarity_ranking_csv)
    df1 = df.reset_index('ID')
    NFT_ID = st.number_input("Enter ID here (only integer from 1 to 10,000)")
    st.write(sell(df_rarity, df1, NFT_ID))
############################################################################
############################################################################
st.header('**Price Predictor**')

option = st.selectbox('Choose a collection from our list of 50',
    ('Bored Ape Yacht Club', 'Doodles', 'Cool Cats', 'Cryptopunks', 'Moonrunners official', 'CopeTown', 'Otherdeed for Otherside',
     'Mutant Ape Yacht Club', 'Moonbirds', 'Primates', 'Dooplicator', 'Azuki', 'Gossamer Seed', 'Solana Monkey Business', 'EDGEHOGS', 'IDZ',
     'The Pilgrims', 'ShitBeast', 'devilvalley', 'LonelyPop', 'The Sandbox', 'Bapes Parental Certificate', 'Scremlins', 'Narentines', 'Udder Chaos',
      'Gutter Cat Gang', 'Kiko Bakes', 'Cool Cats NFT', 'apedog.wtf', 'Town Star', 'Bored Ape Kennel Club', 'Milady Maker', 'Ethlizards', 'NFT Worlds',
      'Art of Mob', 'OzDao Pass', 'Okay Bears', 'Boki', 'Blocksmith Labs', 'Banana Task Force Ape', 'Deafbeef', 'Yeah Tigers', 'FatCats Capital',
       'Meebits', 'OnChainMonkey', 'DeGods', 'FLUF World', 'Decentraland', 'VeeFriends'))

if option == 'Bored Ape Yacht Club':
    sell_function('PricesBoredApeYachtClub.csv', 'Bored.csv', option, 'boredapeyachtclub')
elif option == 'Cryptopunks':
    st.write('content in progress')
elif option == 'Cool Cats':
    st.write('content in progress')
elif option == 'Doodles':
    sell_function('DoodlesPrices.csv', 'Doodles.csv', option, 'doodles-official')
