import sys
import json
import tweepy
import credentials
from tweepy import API
from tweepy import OAuthHandler

# Authorisation
def getHistoricTweets(dictionary, keyword, numOfTweets) :
    i = 0
    try: 
        for tweet in tweepy.Cursor(api.search, q=keyword).items(numOfTweets):
            i = i + 1
            entry = {'Screen-Name': str(tweet.user.screen_name),
                    'Username': (tweet.user.name),
                    'Created-At': str(tweet.created_at),
                    'Text': str(tweet.text),
                    'User-Location': str(tweet.user.location),
                    'Coordinates': str(tweet.coordinates),
                    'Device-Type': str(tweet.source),
                    'Hashtags': str(tweet.entities.get('hashtags')),
                    'Quote-Status': str(tweet.is_quote_status),
                    'Retweeted': str(tweet.retweeted),
                    'Retweet-Count': str(tweet.retweet_count),
                    'Favorited': str(tweet.favorited),
                    'Favorite-Count': str(tweet.favorite_count),
                    'Replied': str(tweet.in_reply_to_status_id_str)
                    }
            dictionary.append(entry)
            print(i)
        print("Done")
        return dictionary
    except tweepy.TweepError as e:
        print("ERROR: " + str(e))

def writeToJson(fileName, dictionary):
    fileName = fileName + '.json'
    with open(fileName, 'w') as file:
        json.dump(dictionary, file)
    print("Written")


if __name__ == "__main__":
    arg_keyword = ' '.join(sys.argv[1])
    arg_json_filename = str(sys.argv[2])

    # Get credentials from credentials.py
    consumer_key = credentials.getConsumerKey()
    consumer_secret = credentials.getConsumerSecret()
    access_token = credentials.getAccessToken()
    access_token_secret = credentials.getAccessTokenSecret()

    # Set Up Auth
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth)
    except Exception as e:
        print("ERROR: Authentication Failed: " + str(e))

    tweetDictionary = []
    keyword = arg_keyword
    print(keyword)
    numOfTweets = 100

    getHistoricTweets(tweetDictionary, keyword, numOfTweets)
    writeToJson(arg_json_filename, tweetDictionary)
