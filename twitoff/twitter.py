
from os import getenv
from .models import db, User, Tweet

import tweepy
import spacy


TWITTER_API_KEY = getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)

twitter = tweepy.API(auth)
nlp = spacy.load("my_nlp_model")

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
    



def get_user_and_Tweet(username):
    user = twitter.get_user(username)
    db_user=User(id=user.id, name=username)
    db.session.add(db_user)
    user_tweets = user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode="Extended")
    for tweet in user_tweets:
        embedding = vectorize_tweet(tweet.text)
        new_tweet=Tweet(id=tweet.id, text=tweet.text, embedding = embedding)
        db_user.tweets.append(new_tweet)
        db.session.add(new_tweet)
    db.session.commit()




