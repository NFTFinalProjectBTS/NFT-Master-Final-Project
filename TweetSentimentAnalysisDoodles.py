#!/usr/bin/env python
# coding: utf-8

# ### Twitter Sentiment Analysis

# In[1]:


# Install necessary libraries
#!pip install textblob


# In[2]:


#!pip install pycountry


# In[3]:


#!pip install langdetect


# In[4]:


# Import necessary libraries
import sys
import tweepy
import re
import string
import os
import pycountry
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from textblob import TextBlob
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from langdetect import detect

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


# In[5]:


#nltk.download('vader_lexicon') # List of lexical features labeled according to their semantic orientation
#nltk.download('stopwords')


# In[6]:


# Authentication to access twitter data

consumer_key = "pnSyCqgVcS1Yml8ierigUJKtL"
consumer_secret = "KcDrwaP2xkfcEXm2GP0ZVJ13VQwGt2mCWQS4Omf9jPi2IVGBcd"
access_token = "1537012839340298241-SKre7utKVfaafIVTkXgMVGv6ATT1P3"
access_token_secret = "dWvlJh8MLncS5UoQ8q0CtoeR74utPrKhqRWr5hcjBACkd"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# ### Retrieving data

# In[10]:


def percentage(part,whole):
    return 100 * float(part)/float(whole) 

# Asking for keywords in tweets as input and the number of tweets we want to analyse
keyword = input("Please enter keyword or hashtag to search: ") 
noOfTweet = int(input ("Please enter how many tweets to analyze: "))

# Initialising lists for the tweets, and the classification as positive, neutral or negative 
tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(noOfTweet)
positive  = 0
negative = 0
neutral = 0
polarity = 0 # This is a score that is assigned to the text to be able to classify it
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

for tweet in tweets:
    tweet_list.append(tweet.text) # Storing the text of the tweets in a list
    analysis = TextBlob(tweet.text) # Use TextBlob library to be able to perform sentiment analysis
    
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text) # Assign scores based on the polarity of the text analysed
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    
    polarity += analysis.sentiment.polarity
    
    if neg > pos:
        negative_list.append(tweet.text)
        negative += 1

    elif pos > neg:
        positive_list.append(tweet.text)
        positive += 1
    
    elif pos == neg:
        neutral_list.append(tweet.text)
        neutral += 1
    else:
        neutral_list.append(tweet.text)
        neutral += 1

positive = percentage(positive, noOfTweet) # Percentage of tweets that have positive notation
negative = percentage(negative, noOfTweet) # Percentage of tweets that have negative notation
neutral = percentage(neutral, noOfTweet) # Percentage of tweets that have neutral notation

positive = format(positive, '.2f')
negative = format(negative, '.2f')
neutral = format(neutral, '.2f')


# The number of tweets analysed is limited for the twitter developer account created.

# In[11]:


# Save tweets in lists based on their polarity

tweet_list = pd.DataFrame(tweet_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)

print("total number of tweets: ",len(tweet_list))
print("positive number: ",len(positive_list))
print("negative number: ", len(negative_list))
print("neutral number: ",len(neutral_list))


# In[12]:


tweet_list


# In[14]:


# Piechart for sentiment distribution in tweets

labels = ['Positive ['+str(positive)+'%]' , 'Neutral ['+str(neutral)+'%]','Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'blue','red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)

plt.style.use('default')
plt.legend(labels)
plt.title("Sentiment Analysis Result for keyword =  "+keyword+"" )
plt.axis('equal')
plt.show()

plt.savefig("sentimentpiechart_doodles.png")


# In[15]:


tweet_list.drop_duplicates(inplace = True)


# In[16]:


# Create a dataframe of the tweets

tw_list = pd.DataFrame(tweet_list)
tw_list


# ### Sentiment analysis

# In[17]:


# # Removing RT, punctuation and other symbols from the text

tw_list["text"] = tw_list[0]

remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
rt = lambda x: re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x)
tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
tw_list["text"] = tw_list.text.str.lower()
tw_list.head(10)


# In[38]:


# Calculating Negative, Positive, Neutral and Compound values

tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))

for index, row in tw_list['text'].iteritems():
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    
    if neg > pos:
        tw_list.loc[index, 'sentiment'] = "negative"
    elif pos > neg:
        tw_list.loc[index, 'sentiment'] = "positive"
    else:
        tw_list.loc[index, 'sentiment'] = "neutral"
        
    tw_list.loc[index, 'neg'] = neg
    tw_list.loc[index, 'neu'] = neu
    tw_list.loc[index, 'pos'] = pos
    tw_list.loc[index, 'compound'] = comp

tw_list.head(10)


# In[19]:


# Creating new data frames for all sentiments (positive, negative and neutral)

tw_list_negative = tw_list[tw_list["sentiment"] == "negative"]
tw_list_positive = tw_list[tw_list["sentiment"] == "positive"]
tw_list_neutral = tw_list[tw_list["sentiment"] == "neutral"]


# In[37]:


tw_list_negative


# In[20]:


all_values = tw_list["text"].values
positive_values = tw_list_positive["text"].values
negative_values = tw_list_negative["text"].values
neutral_values = tw_list_neutral["text"].values


# In[21]:


# Function to create word clouds

def create_wordcloud(sentiment):
    mask = np.array(Image.open("cloud.png"))
    stopwords = nltk.corpus.stopwords.words('english')
    wc = WordCloud(background_color='white',
                  mask = mask,
                  max_words=3000,
                  stopwords=stopwords,
                  repeat=True)
    wc.generate(str(sentiment))
    wc.to_file("wordcloud.png")
    print("Word Cloud Saved Successfully")
    path="wordcloud.png"
    display(Image.open(path))


# In[18]:


# Creating a wordcloud for all tweets

create_wordcloud(all_values)


# In[19]:


# Creating a wordcloud for positive sentiment

create_wordcloud(positive_values)


# In[20]:


# Creating a wordcloud for negative sentiment

create_wordcloud(negative_values)


# In[21]:


# Creating a wordcloud for neutral sentiment
create_wordcloud(neutral_values)


# ### Feature extraction and vectorisation

# In[22]:


# Cleaning Text

stopwords = nltk.corpus.stopwords.words('english') # define stopwords
ps = nltk.PorterStemmer() # create stemmer to stem words

def clean_text(text):
    text_lc = "".join([word.lower() for word in text if word not in string.punctuation]) # remove punctuation
    text_rc = re.sub('[0-9]+', '', text_lc) # remove numbers
    tokens = re.split('\W+', text_rc)    # tokenise text
    text = [ps.stem(word) for word in tokens if word not in stopwords]  # remove stopwords and stem text
    return text


# In[23]:


tw_list['clean'] = tw_list['text'].apply(lambda x: clean_text(x))


# In[24]:


tw_list.head()


# In[25]:


tw_list.to_csv('doodles_sentiment_df.csv')


# In[26]:


# Applying Countvectorizer

countVectorizer = CountVectorizer(analyzer=clean_text) # we use the clean_text function to extract the features from the text
countVector = countVectorizer.fit_transform(tw_list['text'])
print('{} Number of reviews have {} words'.format(countVector.shape[0], countVector.shape[1]))


# In[27]:


# Get a dataframe of the word vectors

count_vect_df = pd.DataFrame(countVector.toarray(), columns=countVectorizer.get_feature_names_out()) # the columns of the df are the words
count_vect_df.drop(columns=count_vect_df.columns[0], axis=1, inplace=True)
count_vect_df


# In[28]:


count_vect_df.to_csv("countvect_doodles.csv")


# In[29]:


# Count of the top 10 most used words in the text

count = pd.DataFrame(count_vect_df.sum())
countdf = count.sort_values(0, ascending=False)
countdf.head(10)


# In[30]:


countdf = countdf.reset_index()


# In[31]:


countdf


# In[32]:


countdf = countdf.rename(columns={'index': 'word', 0: 'count'})


# In[33]:


countdf


# In[34]:


countdf.to_csv("doodles_wordcount.csv")


# In[ ]:




