import re
import sys
import json
import urllib
import urllib.request
import pandas as pd
from textblob import TextBlob 
from collections import Counter

def writeToJson(fileName, dictionary):
    fileName = fileName + '.json'
    with open(fileName, 'w') as file:
        json.dump(dictionary, file)
    print("Written")

def filterOutTweetsWithoutLocation(fileName):
    # We can probably make this method alot nicer
    newFileName = fileName + "-filtered"
    newDict = []

    tweet_json = open(fileName, 'r').read()
    tweet = json.loads(tweet_json)
    json_length = len(tweet)
    index = 0
    # find a way to make this way nicer - list comprehensions?
    for index in range(0, json_length):
        loc = tweet[index]["User-Location"]
        print(loc)
        isCity = False
        isUS = False
        if(loc is ""):
            print("Empty location")
        else:
            with open("./data/cities", 'rb') as f:
                for line in f:
                    if line.decode('utf-8').strip() in loc:
                        print("Contains city: " + line.decode('utf-8').strip() + " in " + loc)
                        isCity = True
                        newDict.append(tweet[index])
                        break
            if (not isCity) :
                with open('./data/us_state_codes') as f1:
                    for line in f1:
                        if line.strip() in loc:
                            print("US state: contains " + line.strip())
                            isUS = True
                            newDict.append(tweet[index])
                            break
            if (not isUS and not isCity) :
                with open('./data/countries') as f2:
                    for line in f2:
                        if line.strip() in loc:
                            print("Country: contains " + line.strip())
                            newDict.append(tweet[index])
                            break
            
        print("---")
    writeToJson(newFileName, newDict)
    return newFileName

def sentimentAnalysis(tweet_info):
    """
    Uses TextBlob https://planspace.org/20150607-textblob_sentiment/
    """
    analysis = TextBlob(tweet_info) 
    # returns (sentiment, subjectivity)
    return analysis.sentiment

def classifier(tweets_with_sentiment):
    duplicateFrequencies = {}
    for i in set(tweets_with_sentiment):
        duplicateFrequencies[i] = tweets_with_sentiment.count(i)
    tweets = duplicateFrequencies.keys()

    df = pd.DataFrame(columns=['tweet', 'sentiment', 'count'])
    for (tweet, sentiment) in tweets:
        count = (duplicateFrequencies.get((tweet, sentiment)))
        df = df.append({'tweet': tweet, 'sentiment': str(sentiment), 'count': count}, ignore_index=True)

    df_to_csv(df, "test.csv")

def df_to_csv(df, csv_name):
    df.to_csv(csv_name, index=True)
    
if __name__ == "__main__":
    file_name = str(sys.argv[1])
    print(file_name)
    file_name = file_name + ".json"
    jsonFile = filterOutTweetsWithoutLocation(file_name)
    print (jsonFile)

    all_tweets = []
    tweet_json = open(file_name, 'r').read()
    tweet = json.loads(tweet_json)
    json_length = len(tweet)
    index = 0
    for index in range(0, json_length):
        tweet_info = tweet[index]
        tweet_text = tweet_info['Text']
        all_tweets.append((tweet_text, sentimentAnalysis(tweet_text)))

    classifier(all_tweets)