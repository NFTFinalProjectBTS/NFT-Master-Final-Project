def func(collection_name):# Enter the name of the collection, as in OpenSea (for example web('azuki'), we take the name from https://opensea.io/collection/azuki).

    #NFT rank web scraping using BeautifulSoup from https://ranknft.io/
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup

    lst = []
    #Loop to view each NFT collection
    for i in range(0,10000):
        url = f'https://ranknft.io/item/{collection_name}/{i}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        lst1=[]
        #Loop to view each NFT element
        for word in soup.find_all('h2'):#Search all elements with a tag h2
                
                word = word.get_text() #Getting elements
  
                lst1.append(word)#Adding elements to the list
                
        lst.append(lst1)
    
    Rank = pd.DataFrame(lst)
    #Frame clearing
    Rank[1]  = Rank[1] .str.replace(r"[^\d\.]", "", regex=True)
    Rank[2]  = Rank[2] .str.replace(r"[^\d\.]", "", regex=True)
    #Renaming columns
    Rank.rename(columns = {0 : 'Name_collection', 1 : 'id_elements', 2 : 'Rank', 3 : 'Score', 4 : 'Items'}, inplace = True) 
    Rank['Name_collection'] = f'{collection_name}'
    #Removing a column with the number of elements in the collection
    Rank.drop(5, inplace=True, axis=1)
    #Save to csv
    Rank.to_csv(f'{collection_name}.csv')
    # Get dataset with Collection rank, Item rarity score, Item traits
    
    return print('ready') 

func('mfers')