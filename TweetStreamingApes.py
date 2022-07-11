#!/usr/bin/env python
# coding: utf-8

# ### Real-Time Twitter Data

# In[1]:


from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json
from collections import namedtuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[9]:


# Create the Spark and the Streaming Contexts with the time frame to retrieve the tweets, in this case 1 minute
sc = SparkContext("local[2]", "tweets")
ssc = StreamingContext(sc, 60)

# Define the fields we will use to create our temporary tables
fields = ("created_at","text")
Tweet = namedtuple('Tweet', fields )

# Create a window to get tweets even if in the minute that the context is set there are no tweets posted
lines = ssc.socketTextStream("localhost", 9999).window(120, 60)

# Filter the text of the tweets to get the hashtags and count the times they appear
tweets = lines.map(lambda x: json.loads(x)).map(lambda x: Tweet(x['created_at'],x['text']))
hashtags = tweets.filter(lambda line: "#" in line.text).flatMap(lambda line: [word for word in line.text.split(" ") if word.startswith("#")])
hashtag_count = hashtags.map(lambda mention: mention, 1).countByValue()

# Create a temporary table with the hashtags and their count
hashtag_df = hashtag_count.foreachRDD( lambda rdd: rdd.toDF().registerTempTable("hashtags"))

# Count how many tweets have been posted and save them in a temporary table
tweet_count = tweets.count()
tweets_df = tweet_count.foreachRDD( lambda rdd: rdd.toDF().registerTempTable("tweets"))

hashtag_count.pprint()
tweet_count.pprint()

ssc.start()
#ssc.awaitTermination()


# In[87]:


ssc.stop() # Every time we want to run the contexts we should stop the current ones
sc.stop()


# In[57]:


from pyspark.sql import SQLContext

sqlContext = SQLContext(sc) # Inside the Spark Context cluster we create a SQL context to query the data in the temporary table
sqlContext.sql('select * from hashtags').show()


# In[58]:


hashtag = sqlContext.sql('select * from hashtags').collect()


# In[59]:


df_hashtag = pd.DataFrame(columns=['hashtag','n_total'])

for i,h in enumerate(hashtag):
    hash_ = h[0]
    count_n = h[1]
    df_hashtag.loc[i]=[hash_,count_n]
    #tuple_hashtag = (hash_,count_n)
    #df_hashtag.append(hash_, count_n)


# In[60]:


df_hashtag.reset_index()


# In[65]:


df_hashtag['hashtag2'] = ''

df_1 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('nft')]
list_nft = list(df_1.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_nft),'#NFT',df_hashtag['hashtag2'])

df_2 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('bored')]
list_crypto = list(df_2.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_crypto),'#BoredApes',df_hashtag['hashtag2'])

df_3 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('eth')]
list_eth = list(df_3.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_eth),'#ETH',df_hashtag['hashtag2'])

df_4 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('opensea')]
list_opensea = list(df_4.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_opensea),'#Opensea',df_hashtag['hashtag2'])

df_5 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('bayc')]
list_blockchain = list(df_5.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_blockchain),'#BoredApes',df_hashtag['hashtag2'])

df_6 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('crypto')]
list_blockchain = list(df_6.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_blockchain),'#Cryptocurrencies',df_hashtag['hashtag2'])

df_hashtag['hashtag2'] = np.where(df_hashtag['hashtag2'] == '','other',df_hashtag['hashtag2'])


# In[66]:


df_hashtag


# In[67]:


df_hashtag.to_csv('boredapes_hashtags.csv')


# In[68]:


df_hashtag


# In[69]:


df = df_hashtag.groupby(['hashtag2']).agg(total_hashtag=('n_total','sum'))


# In[70]:


df


# In[71]:


df = df.reset_index()


# In[72]:


df = df.sort_values('total_hashtag', ascending = False)


# In[73]:


df


# In[74]:


df = df.rename(columns={"hashtag2": "hashtag", "total_hashtag": "count"})


# In[75]:


df


# In[76]:


df['count'].sum()


# In[77]:


df.to_csv('df_hashtag_boredapes.csv')


# In[78]:


# drop rows that appear just once
#a = ['other']
#df = df[~df['hashtag'].isin(a)]


# In[79]:


df['percentage'] = round((df['count']/df['count'].sum())*100,2)


# In[80]:


df


# In[81]:


df.to_csv('boredapes_hashtag_perc_2.csv')


# In[83]:


names = ["Others", "BoredApes", "#Cryptocurrencies", "#NFT"]


# In[86]:


plot = df.plot.pie(y='count', title="Percentage", labels = names, legend=True,                    autopct='%1.1f%%',                    shadow=True, startangle=0)
plt.savefig("cryptopunks_twpie.png")


# In[85]:


#TOP HASHTAGS

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
 
objects = df['hashtag']
y_pos = np.arange(len(objects))
count = df['count']
 
plt.barh(y_pos, count, align='center', alpha=0.5, color="navy")
plt.yticks(y_pos, objects)
plt.xlabel('Count')
plt.title('Top Hashtag Tweets')
 
plt.show()
plt.savefig('top_hashtags.png')


# In[ ]:




