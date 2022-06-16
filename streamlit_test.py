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
st.title('NiFTy.1')

st.header('**Welcome to our NFT comparison tool!**')

option = st.selectbox('Choose a collection to display common info',
    ('Bored Ape Yacht Club', 'Cryptopunks', 'Cool Cats', 'Doodles'))

def create_columns(item, owners, floor_price, total_volume):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Items", item)
    col2.metric("Owners", owners)
    col3.metric("Floor Price (ETH)", floor_price)
    col4.metric("Total Volume (ETH)", total_volume)
###############################################################################
###############################################################################
def content(full_collection_csv, rarity_ranking_csv, collection_name, collection_slug):
    st.subheader('General information about the collection')
    st.write(collection_info(collection_slug)[2])
    st.write('-' * 30)
    st.subheader('''Collection's logo''')
    collection_image = collection_info(collection_slug)[1]
    if collection_image.endswith('mp4') or collection_image.endswith('mov'):
        st.video(collection_image)
    elif collection_image.endswith('svg'):
        svg = requests.get(collection_image).content.decode()
        st.image(svg)
    elif collection_image:
        st.image(collection_image)
    st.write('-' * 30)
    st.subheader('Key metrics')
    #fetching the metrics from the collection_info function
    _, _, _, items, owners, floor_price, total_volume = collection_info(collection_slug)
    create_columns(items, owners, floor_price, total_volume)
    st.write('-' * 30)
    df = NFT_analysis(collection_name, collection_slug, full_collection_csv, rarity_ranking_csv)
    st.write('Below is a list of the sniped NFTs for this collection. These are the NFTs with the best price/rarity ratio')
    #returning the df_sniped
    df_sniped_st = clustering(df, collection_name)[1]
    st.dataframe(df_sniped_st)

    #download the data as a csv button
    def convert_df(df):
         return df.to_csv().encode('utf-8')
    csv = convert_df(df_sniped_st)
    st.download_button(
         label="Download data as CSV",
         data=csv,
         file_name=f'{collection_name}_sniped.csv',
         mime='text/csv',)

    st.write('-' * 30)
    #displaying the figure form the plotted clustering
    st.pyplot(clustering(df, collection_name)[2])
    st.write('-' * 30)
    st.header('**Sell function**')
    st.write('Provide an NFT ID and it will predict a price based on its rarity compared to similar rarities in the collection')
    df_rarity = dataframe_cleaning_rankings(rarity_ranking_csv)
    df1 = df.reset_index('ID')
    NFT_ID = st.number_input("Enter ID here (only integer from 1 to 10,000)")
    st.write(sell(df_rarity, df1, NFT_ID))

###############################################################################
#######################CALLING THE CONTENT FUNCTION############################
###############################################################################
##############################################################################################################################################################
if option == 'Bored Ape Yacht Club':
    content('PricesBoredApeYachtClub.csv', 'Bored.csv', option, 'boredapeyachtclub')
elif option == 'Cryptopunks':
    #content()
    st.write('content in progress')
elif option == 'Cool Cats':
    #content()
    st.write('content in progress')
elif option == 'Doodles':
    content('DoodlesPrices.csv', 'Doodles.csv', option, 'doodles-official')
