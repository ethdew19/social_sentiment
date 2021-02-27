import praw
import requests
import os
import re
from os import environ
from textblob import TextBlob
from tweepy import *


access_token = environ.get('access_token')
access_token_secret = environ.get('secret_access')
consumer_key = environ.get('consumer_key')
consumer_secret = environ.get('consumer_secret')
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

secret = environ.get('secret')
client_id = environ.get('client_id')
user_agent = "Top Post Finder 1.0 by /u/xEquator"
reddit = praw.Reddit(client_id=client_id, client_secret=secret, user_agent=user_agent)

#n is amount of posts to go through, since this doesn't ignore pinned posts you will want at least 3
#Search terms should be the ticker(ie 'btc') and the actual name (ie 'bitcoin')
#Returns list with sentiment of each post
def reddit_sentiment(n, search_term1, search_term2) :
    sentiment_tracker = []
    for submission in reddit.subreddit("cryptocurrency").hot(limit=n):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if len(re.findall(search_term1, comment.body, flags=re.IGNORECASE)) > 0 or len(re.findall(search_term2, comment.body,  flags=re.IGNORECASE)) > 0:
                g = TextBlob(comment.body)
                sentiment_tracker.append(g.sentiment.polarity)
    return sentiment_tracker
#Returns list of sentiment from each tweet
#n is amount of tweets to go through
#term can be used with a hashtag ('#btc')
def twitter_sentiment(n, term) :
    sentiment_tracker = []
    tweets = Cursor(api.search,q=term,lang="en").items(n)
    for tweet in tweets:
        h = TextBlob(tweet.text)
        sentiment_tracker.append(h.sentiment.polarity)
    return sentiment_tracker
#simpe function that finds mean of list of numbers
def mean_of_list(a):
    total = 0
    for x in a:
        total += x
    return total / len(a)

#takes list of floats, finds mean and returns the overall sentiment
def sentiment_analysis(a):
    mean_sentiment = mean_of_list(a)
    if mean_sentiment < -.8 :
        final_sentiment = "Overwhelmingly Negative"
    elif mean_sentiment < -.4 and mean_sentiment >= -.8:
        final_sentiment = "Fairly Negative"
    elif mean_sentiment < 0 and mean_sentiment >= -.4:
        final_sentiment = "Slightly Negative"
    elif mean_sentiment == 0:
        final_sentiment = "Neutral"
    elif mean_sentiment < .4 and mean_sentiment > 0:
        final_sentiment = "Slightly Positive"
    elif mean_sentiment < .8 and mean_sentiment >= .4:
        final_sentiment = "Fairly Positive"
    elif mean_sentiment < .8 :
        final_sentiment = "Overwhelmingly Positive"
    
    return("Sentiment is " + final_sentiment + " (" + str(mean_sentiment) + ")" + " with sample size of " + str(len(a)))

#examples 
#print(sentiment_analysis(reddit_sentiment(5, 'btc', "bitcoin")))
#print(sentiment_analysis(twitter_sentiment(100,'btc')))