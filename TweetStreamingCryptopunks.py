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


# In[47]:


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


# In[113]:


ssc.stop() # Every time we want to run the contexts we should stop the current ones
sc.stop()


# In[58]:


from pyspark.sql import SQLContext

sqlContext = SQLContext(sc) # Inside the Spark Context cluster we create a SQL context to query the data in the temporary table
sqlContext.sql('select * from hashtags').show()


# In[63]:


hashtag = sqlContext.sql('select * from hashtags').collect()


# In[91]:


df_hashtag = pd.DataFrame(columns=['hashtag','n_total'])

for i,h in enumerate(hashtag):
    hash_ = h[0]
    count_n = h[1]
    df_hashtag.loc[i]=[hash_,count_n]
    #tuple_hashtag = (hash_,count_n)
    #df_hashtag.append(hash_, count_n)


# In[92]:


df_hashtag.reset_index()


# In[93]:


df_hashtag['hashtag2'] = ''

df_1 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('nft')]
list_nft = list(df_1.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_nft),'#NFT',df_hashtag['hashtag2'])

df_2 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('cryptopunks')]
list_crypto = list(df_2.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_crypto),'#Cryptopunks',df_hashtag['hashtag2'])

df_3 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('eth')]
list_eth = list(df_3.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_eth),'#ETH',df_hashtag['hashtag2'])

df_4 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('opensea')]
list_opensea = list(df_4.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_opensea),'#Opensea',df_hashtag['hashtag2'])

df_5 = df_hashtag[df_hashtag['hashtag'].str.lower().str.contains('blockchain')]
list_blockchain = list(df_5.index)
df_hashtag['hashtag2'] = np.where(df_hashtag.index.isin(list_blockchain),'#Blockchain',df_hashtag['hashtag2'])

df_hashtag['hashtag2'] = np.where(df_hashtag['hashtag2'] == '','other',df_hashtag['hashtag2'])


# In[94]:


df_hashtag


# In[95]:


df_hashtag.to_csv('cryptopunks_hashtags.csv')


# In[96]:


df_hashtag


# In[97]:


df = df_hashtag.groupby(['hashtag2']).agg(total_hashtag=('n_total','sum'))


# In[98]:


df


# In[99]:


df = df.reset_index()


# In[100]:


df = df.sort_values('total_hashtag', ascending = False)


# In[101]:


df


# In[102]:


df = df.rename(columns={"hashtag2": "hashtag", "total_hashtag": "count"})


# In[103]:


df


# In[104]:


df['count'].sum()


# In[105]:


df.to_csv('df_hashtag_cryptopunks.csv')


# In[106]:


# drop rows that appear just once
#a = ['other']
#df = df[~df['hashtag'].isin(a)]


# In[107]:


df['percentage'] = round((df['count']/df['count'].sum())*100,2)


# In[108]:


df


# In[114]:


df.to_csv('cryptopunks_hashtag_perc_2.csv')


# In[110]:


names = ["#NFT",  "#Cryptopunks", "#ETH", "Others",]


# In[111]:


plot = df.plot.pie(y='count', title="Percentage", labels = names, legend=True,                    autopct='%1.1f%%',                    shadow=True, startangle=0)
plt.savefig("cryptopunks_twpie.png")


# In[112]:


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




