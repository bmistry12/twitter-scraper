import sys
import json
import pandas as pd
import utils
from textblob import TextBlob


def _classifier(tweets_with_sentiment, locations, output_csv):
    """Classify each tweet with a sentiment."""
    duplicate_freq = {}
    for item in set(tweets_with_sentiment):
        duplicate_freq[item] = tweets_with_sentiment.count(item)
    tweets = duplicate_freq.keys()
    df = pd.DataFrame(columns=['tweet', 'sentiment', 'count'])
    for index, (tweet, sentiment) in enumerate(tweets):
        count = (duplicate_freq.get((tweet, sentiment)))
        loc = locations[index]
        df = df.append({'tweet': tweet, 'sentiment': str(
            sentiment), 'count': count, 'location': loc}, ignore_index=True)
    utils.df_to_csv(df, output_csv)


def _filter_known_locations(file_name):
    """Get tweets with a known location."""
    filtered_file_name = file_name + "-filtered"
    known_locations = tweets_with_known_location = []
    with open(file_name, 'r') as tweet_file:
        tweet_json = tweet_file.read()
    tweet = json.loads(tweet_json)
    with open("./data/cities", 'rb') as city_file:
        known_locations += city_file.readlines()
    with open('./data/us_state_codes', 'rb') as us_file:
        known_locations += us_file.readlines()
    with open('./data/countries', 'rb') as country_file:
        known_locations += country_file.readlines()
    for index in enumerate(tweet):
        loc = tweet[index]["User-Location"]
        if loc == "" or loc is None:
            print("Empty location")
            continue
        for line in known_locations:
            if line.decode('utf-8').strip() in loc:
                print(line.decode('utf-8').strip() + " in " + loc)
                tweets_with_known_location.append(tweet[index])
                break
        print("---")
    utils.write_to_json(filtered_file_name, tweets_with_known_location)
    return filtered_file_name


def _sentiment_analyis(tweet_text):
    """Perform sentiment analysis with TextBlob.
    https://planspace.org/20150607-textblob_sentiment/.
    """
    analysis = TextBlob(tweet_text)
    # returns (sentiment, subjectivity)
    return analysis.sentiment


if __name__ == "__main__":
    file_name = str(sys.argv[1]) + ".json"
    output_csv = str(sys.argv[2])
    json_file = _filter_known_locations(file_name)
    all_tweets = all_loc = []

    with open(file_name) as tweet_file:
        tweet_json = tweet_file.read()
    json_tweets = json.loads(tweet_json)
    for index in enumerate(json_tweets):
        tweet_info = json_tweets[index]
        tweet_text = tweet_info['Text']
        tweet_loc = tweet_info["User-Location"]
        all_tweets.append((tweet_text, _sentiment_analyis(tweet_text)))
        all_loc.append(tweet_loc)

    _classifier(all_tweets, all_loc, output_csv)
