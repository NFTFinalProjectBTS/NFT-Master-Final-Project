#function that estimates the price of an NFT, based on a subset of NFTs with similar rarity

def sell(df_rarity, df1, ID):

    #sorting the df, indexing by ID
    df_rarity1 = df_rarity.sort_values(by='ID').set_index('ID')
    #fetching the rarity according the the given ID
    rarity = df_rarity1.loc[ID, 'rarity']

    #creating a rarity range subset
    rarity_inf = rarity - 500
    rarity_sup = rarity + 500

    #filtering the df with the rarity range then getting the mean price
    price = df1[(df1['rarity'] > rarity_inf) & (df1['rarity'] < rarity_sup)]['Price'].mean()

    output = f'Your NFT, with ID **#{ID}** and a rarity ranking of **{rarity}** has an estimated price of **${int(price)}**'

    return output
