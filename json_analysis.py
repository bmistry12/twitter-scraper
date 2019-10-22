import re
import sys
import json
import urllib
import urllib.request

def writeToJson(fileName, dictionary):
    fileName = fileName + '.json'
    with open(fileName, 'w') as file:
        json.dump(dictionary, file)
    print("Written")

def filterOutTweetsWithoutLocation(fileName):
    # We can probably make this alot nicer
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

def ranking(tweet_info):
    rankCount = 0
    # step 1 - if is RT then the tweet exists elsewhere - this will increase a value called "importance"
    text = tweet_info["Text"]
    if text[:2] == 'RT':
        rankCount = rankCount + 1
    # step 2 - favourite count will increase importance
    return rankCount

def sentimentAnalysis(tweet_info):
    # analyse if text is positive or negative ...
    # if positive give score of 1
    # if negative give score of 0
    pass

if __name__ == "__main__":
    file_name = str(sys.argv[1])
    print(file_name)
    # file_name = file_name + ".json"
    jsonFile = filterOutTweetsWithoutLocation(file_name)
    print (jsonFile)

# all_tweets = []

# tweet_json = open(jsonFile, 'r').read()
# tweet = json.loads(tweet_json)
# json_length = len(tweet)
# index = 0
# for index in range(0, json_length):
#     tweet_info = tweet[index]
#     all_tweets.append(index, ranking(tweet_info), sentimentAnalysis(tweet_info))
