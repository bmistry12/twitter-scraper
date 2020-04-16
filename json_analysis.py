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
        isCity = False
        isUS = False
        if loc == "":
            print("Empty location")
        else:
            with open("./data/cities", 'rb') as f:
                for line in f:
                    if line.decode('utf-8').strip() in loc:
                        print("Contains city: " + line.decode('utf-8').strip() + " in " + loc)
                        isCity = True
                        newDict.append(tweet[index])
                        break
            if not isCity:
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

def sentimentAnalysis(tweet_text):
    """
    Uses TextBlob https://planspace.org/20150607-textblob_sentiment/
    """
    analysis = TextBlob(tweet_text) 
    # returns (sentiment, subjectivity)
    return analysis.sentiment

def classifier(tweets_with_sentiment, locations, output_csv):
    duplicateFrequencies = {}
    for i in set(tweets_with_sentiment):
        duplicateFrequencies[i] = tweets_with_sentiment.count(i)
    tweets = duplicateFrequencies.keys()

    df = pd.DataFrame(columns=['tweet', 'sentiment', 'count'])
    for index, (tweet, sentiment) in enumerate(tweets):
        count = (duplicateFrequencies.get((tweet, sentiment)))
        loc = locations[index]
        df = df.append({'tweet': tweet, 'sentiment': str(sentiment), 'count': count, 'location': loc}, ignore_index=True)

    df_to_csv(df, output_csv)

def df_to_csv(df, csv_name):
    df.to_csv(csv_name, index=True)
    
if __name__ == "__main__":
    file_name = str(sys.argv[1])
    output_csv = str(sys.argv[2])
    print(file_name)
    file_name = file_name + ".json"
    jsonFile = filterOutTweetsWithoutLocation(file_name)
    print (jsonFile)

    all_tweets = []
    all_loc = []
    tweet_json = open(file_name, 'r').read()
    tweets = json.loads(tweet_json)
    json_length = len(tweets)
    index = 0
    for index in range(0, json_length):
        tweet_info = tweets[index]
        tweet_text = tweet_info['Text']
        tweet_loc = tweet_info["User-Location"]
        all_tweets.append((tweet_text, sentimentAnalysis(tweet_text)))
        all_loc.append(tweet_loc)

    classifier(all_tweets, all_loc, output_csv)