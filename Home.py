from Main import *
from sell import *
from clustering import *
from API_collection_info import *
from For_graph import *
############################################################################
############################################################################
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
############################################################################
############################################################################
############################################################################
img = Image.open('nifty1_logo.png')
st.set_page_config(page_title='NiFTy.1', page_icon=img)

#st.markdown("<h1 style='text-align: center; color: orange;'>NiFTy.1</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.write("")
with col2:
    st.image(img)
with col3:
    st.write("")

st.header('**Welcome to your NFT analytics platform!**')

option = st.selectbox('Choose a collection to display common info',
    ('Bored Ape Yacht Club', 'Doodles', 'Cool Cats', 'Cryptopunks', 'Moonrunners official', 'CopeTown', 'Otherdeed for Otherside',
     'Mutant Ape Yacht Club', 'Moonbirds', 'Primates', 'Dooplicator', 'Azuki', 'Gossamer Seed', 'Solana Monkey Business', 'EDGEHOGS', 'IDZ',
     'The Pilgrims', 'ShitBeast', 'devilvalley', 'LonelyPop', 'The Sandbox', 'Bapes Parental Certificate', 'Scremlins', 'Narentines', 'Udder Chaos',
     'Gutter Cat Gang', 'Kiko Bakes', 'Cool Cats NFT', 'apedog.wtf', 'Town Star', 'Bored Ape Kennel Club', 'Milady Maker', 'Ethlizards', 'NFT Worlds',
     'Art of Mob', 'OzDao Pass', 'Okay Bears', 'Boki', 'Blocksmith Labs', 'Banana Task Force Ape', 'Deafbeef', 'Yeah Tigers', 'FatCats Capital',
     'Meebits', 'OnChainMonkey', 'DeGods', 'FLUF World', 'Decentraland', 'VeeFriends'))

def general_info_columns(collection_image, collection_description):
    col1, col2 = st.columns([1,3])
    with col1:
        st.subheader('Logo')
        if collection_image.endswith('mp4') or collection_image.endswith('mov'):
            st.video(collection_image)
        elif collection_image.endswith('svg'):
            svg = requests.get(collection_image).content.decode()
            st.image(svg)
        elif collection_image:
            st.image(collection_image)
    with col2:
        st.subheader('General information about the collection')
        st.write(collection_description)

def metric_columns(item, owners, floor_price, total_volume):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Items", item)
    col2.metric("Owners", owners)
    col3.metric("Floor Price (ETH)", floor_price)
    col4.metric("Total Volume (ETH)", total_volume)

def images_columns(urls, token_id, prices, rarities):
    col1, col2, col3, col4, col5 = st.columns(5)

    column_list = [col1, col2, col3, col4, col5]

    for i, column in enumerate(column_list):
        with column:
            st.write(f'#{token_id[i]}')
            st.image(urls[i])
            st.write(f'Price :', prices[i])
            st.write('Rarity :', rarities[i])
##############################################################################
###############################################################################
def content(full_collection_csv, rarity_ranking_csv, collection_name, collection_slug, urls_5, token_ids_5, prices, rarities):
    #calling the variables from the 'collection_info' function
    _, collection_image, collection_description, items, owners, floor_price, total_volume, traits = collection_info(collection_slug)
    general_info_columns(collection_image, collection_description)
    st.write('-' * 30)
    st.subheader('Key metrics')
    metric_columns(items, owners, floor_price, total_volume)
    st.write('-' * 30)
    #displaying the figure form the plotted clustering
    df = NFT_analysis(collection_name, collection_slug, full_collection_csv, rarity_ranking_csv)
    st.pyplot(clustering(df, collection_name)[2])
    st.write('-' * 30)
    st.write('Below is a list of the sniped NFTs for this collection. These are the NFTs with the best price/rarity ratio.')
    #returning the df_sniped
    df_sniped_st = (clustering(df, collection_name)[1]).head(10)
    #download the data as a csv button
    csv = df_sniped_st.to_csv().encode('utf-8')
    st.download_button(
         label="Download data as CSV",
         data=csv,
         file_name=f'{collection_name}_sniped.csv',
         mime='text/csv')
    images_columns(urls_5, token_ids_5, prices, rarities)
    st.write('1 ETH = 1 227,88 USD on 11/07/2022')
    st.write('-' * 30)
    st.header('**Traits**')
    st.write('''Below is a list of all the traits of the collection.
                Expand each of them to find the different attributes within each trait and their number of appearance.''')
    traits_list = list(traits.keys())
    for i in traits_list:
        with st.expander(i.capitalize()):
            st.write(traits[i])

###############################################################################
#######################CALLING THE CONTENT FUNCTION############################
###############################################################################
###############################################################################
#BORED APE YACHT CLUB
df_bored_images = pd.read_csv('bored_apes_images.csv')
urls_bored = df_bored_images['image_thumbnail_url'][:5]
token_ids_bored = df_bored_images['token_id'][:5]
prices_bored = ['84 ETH', '84 ETH', '86 ETH', '86 ETH', '84 ETH']
rarities_bored = ['3906', '6382', '2505', '2936', '6807']

urls_10 = df_bored_images['image_thumbnail_url'][5:]
token_ids_10 = df_bored_images['token_id'][5:]

#Doodles
df_doodles_images = pd.read_csv('doodles_images.csv')
urls_doodles = df_doodles_images['image_thumbnail_url']
token_ids_doodles = df_doodles_images['token_id']
prices_doodles = ['12,6 ETH', '12,7 ETH', '13 ETH', '12,6 ETH', '12,75 ETH']
rarities_doodles = ['5708', '726', '3841', '2069', '4968']
###############################################################################

if option == 'Bored Ape Yacht Club':
    content('PricesBoredApeYachtClub.csv', 'Bored.csv', option, 'boredapeyachtclub', urls_bored, token_ids_bored, prices_bored, rarities_bored)
elif option == 'Cryptopunks':
    #content()
    st.write('content in progress')
    st.pyplot(price_punk(punks))
elif option == 'Cool Cats':
    #content()
    st.write('content in progress')
elif option == 'Doodles':
    content('DoodlesPrices.csv', 'Doodles.csv', option, 'doodles-official', urls_doodles, token_ids_doodles, prices_doodles, rarities_doodles)
