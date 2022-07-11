import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
############################################################################
############################################################################
st.title('Twitter feed analysis')

#st.write('''This table shows the hashtags gotten from twitter in a span of
#a minute related to nfts, ethereum and cryptocurrencies''')

df_hashtag_3 = pd.read_csv('df_hashtag_3.csv')
df_hashtag_3.drop(['Unnamed: 0'], axis=1, inplace=True)
#st.dataframe(df_hashtag_3)

#st.write('-' * 30)

st.write("""In a 1-minute span, this is the ditribution of NFT-related hashtags. In Tweets that contain at least one NFT-related hashtag,
the 'Others' category group the hashtags that doesn't contain our selected filtering keywords.""")

img = Image.open('hashtag_pie_3.png')
st.image(img)

st.write('-' * 30)

option = st.selectbox('Choose a collection from our list of 50',
    ('Bored Ape Yacht Club', 'Doodles', 'Cool Cats', 'Cryptopunks', 'Moonrunners official', 'CopeTown', 'Otherdeed for Otherside',
     'Mutant Ape Yacht Club', 'Moonbirds', 'Primates', 'Dooplicator', 'Azuki', 'Gossamer Seed', 'Solana Monkey Business', 'EDGEHOGS', 'IDZ',
     'The Pilgrims', 'ShitBeast', 'devilvalley', 'LonelyPop', 'The Sandbox', 'Bapes Parental Certificate', 'Scremlins', 'Narentines', 'Udder Chaos',
      'Gutter Cat Gang', 'Kiko Bakes', 'Cool Cats NFT', 'apedog.wtf', 'Town Star', 'Bored Ape Kennel Club', 'Milady Maker', 'Ethlizards', 'NFT Worlds',
      'Art of Mob', 'OzDao Pass', 'Okay Bears', 'Boki', 'Blocksmith Labs', 'Banana Task Force Ape', 'Deafbeef', 'Yeah Tigers', 'FatCats Capital',
       'Meebits', 'OnChainMonkey', 'DeGods', 'FLUF World', 'Decentraland', 'VeeFriends'))

if option == 'Bored Ape Yacht Club':
    st.write('Adding the collection name as a filtering hashtag keyword')
    img_apes = Image.open('apes_pie.png')
    st.image(img_apes)
elif option == 'Cryptopunks':
    st.write('Adding the collection name as a filtering hashtag keyword')
    img_cryptopunks = Image.open('punks_pie.png')
    st.image(img_cryptopunks)
elif option == 'Cool Cats':
    st.write('content in progress')
elif option == 'Doodles':
    st.write('Adding the collection name as a filtering hashtag keyword')
    img_doodles = Image.open('doodles_pie.png')
    st.image(img_doodles)
