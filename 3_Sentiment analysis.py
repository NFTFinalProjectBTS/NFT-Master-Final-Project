import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
############################################################################
############################################################################
st.title('Sentiment analysis')

option = st.selectbox('Choose a collection from our list of 50',
    ('Bored Ape Yacht Club', 'Doodles', 'Cool Cats', 'Cryptopunks', 'Moonrunners official', 'CopeTown', 'Otherdeed for Otherside',
     'Mutant Ape Yacht Club', 'Moonbirds', 'Primates', 'Dooplicator', 'Azuki', 'Gossamer Seed', 'Solana Monkey Business', 'EDGEHOGS', 'IDZ',
     'The Pilgrims', 'ShitBeast', 'devilvalley', 'LonelyPop', 'The Sandbox', 'Bapes Parental Certificate', 'Scremlins', 'Narentines', 'Udder Chaos',
      'Gutter Cat Gang', 'Kiko Bakes', 'Cool Cats NFT', 'apedog.wtf', 'Town Star', 'Bored Ape Kennel Club', 'Milady Maker', 'Ethlizards', 'NFT Worlds',
      'Art of Mob', 'OzDao Pass', 'Okay Bears', 'Boki', 'Blocksmith Labs', 'Banana Task Force Ape', 'Deafbeef', 'Yeah Tigers', 'FatCats Capital',
       'Meebits', 'OnChainMonkey', 'DeGods', 'FLUF World', 'Decentraland', 'VeeFriends'))

if option == 'Bored Ape Yacht Club':
    col1, col2 = st.columns(2)
    with col1:
        df_apes_WC = pd.read_csv('apes_wordcount.csv')
        df_apes_WC.drop(['Unnamed: 0'], axis=1, inplace=True)
        st.dataframe(df_apes_WC)
    with col2:
        st.write('Positive: 40,70%')
        st.write('Neutral: 9,10%')
        st.write('Negative: 50,20%')
elif option == 'Cryptopunks':
    col1, col2 = st.columns(2)
    with col1:
        df_cryptopunks_WC = pd.read_csv('cryptopunks_wordcount.csv')
        df_cryptopunks_WC.drop(['Unnamed: 0'], axis=1, inplace=True)
        st.dataframe(df_cryptopunks_WC)
    with col2:
        st.write('Positive: 15,33%')
        st.write('Neutral: 77,87%')
        st.write('Negative: 6,80%')
elif option == 'Cool Cats':
    st.write('content in progress')
elif option == 'Doodles':
    col1, col2 = st.columns(2)
    with col1:
        df_doodles_WC = pd.read_csv('doodles_wordcount.csv')
        df_doodles_WC.drop(['Unnamed: 0'], axis=1, inplace=True)
        st.dataframe(df_doodles_WC)
    with col2:
        st.write('Positive: 61,80%')
        st.write('Neutral: 35,85%')
        st.write('Negative: 2,35%')
