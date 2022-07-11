#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
import json
import tweepy


# In[2]:


# Define authentication keys for the Twitter API
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAH%2F7dwEAAAAA2CKaw7TJqPIAs8pATYlXjUN0qc4%3Dm751IcZOxIB4BbmWNwTyVaZ51Taecp76Xu7k0cuzotPynV05Us'
streaming_client = tweepy.StreamingClient(bearer_token)


# In[9]:


# set up the socket, the host machine and the port to use for the retrieve of real-time tweets
s = socket.socket()
host = 'localhost'
port = 9999

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) # With this we are able to run several times the code using the same port
s.bind((host, port))

print('listening on port: %s' % str(port)) # Print this line to check the socket is set up correctly

s.listen() 
class TweetsPrinter(tweepy.StreamingClient):
# Define the items we want to retrieve from the tweets, like the text and the date they were posted
    def on_tweet(self, tweet):
        c, addr = s.accept()
        my_object = {
            'created_at': tweet.created_at,
            'text': tweet.text,
        }
        json_encoded = json.dumps(my_object, default=str) # Encode the tweets as json files to print them
        c.send(json_encoded.encode('utf-8'))
        c.close()
        print(json_encoded)

        
# Add rules to filter tweets by desired hashtags
printer = TweetsPrinter(bearer_token)
#printer.add_rules(tweepy.StreamRule('#NFT'))
printer.add_rules(tweepy.StreamRule('#BAYC'))
printer.add_rules(tweepy.StreamRule('#boredapes'))
printer.add_rules(tweepy.StreamRule('#boredapesyachtclub'))
printer.filter(tweet_fields=['created_at','text'])


# In[8]:


# Every time we want to filter for different hashtags we should run this to delete previous filters
printer.delete_rules([x.id for x in printer.get_rules().data])


# In[ ]:




