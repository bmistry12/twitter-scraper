import sys
import json
import utils
import pandas as pd
from textblob import TextBlob


def _classifier(tweets_with_sentiment, locations, output_csv):
    """Classify each tweet with a sentiment."""
    print("Classifying...")
    duplicate_freq = {}
    for item in set(tweets_with_sentiment):
        duplicate_freq[item] = tweets_with_sentiment.count(item)
    tweets = duplicate_freq.keys()
    df = pd.DataFrame(columns=['tweet', 'sentiment', 'count'])
    for index, item in enumerate(tweets):
        if not isinstance(item, tuple):
            continue
        tweet, sentiment = item
        count = (duplicate_freq.get((tweet, sentiment)))
        loc = locations[index]
        df = df.append({'tweet': tweet, 'sentiment': str(
            sentiment), 'count': count, 'location': loc}, ignore_index=True)
    utils.df_to_csv(df, output_csv)


def _filter_known_locations(file_name):
    """Get tweets with a known location."""
    print("Getting tweets with known location...")
    filtered_file_name = file_name + "-filtered"
    known_locations = []
    tweets_with_known_location = []
    with open(file_name, 'r', encoding="utf-8") as tweet_file:
        tweet_json = tweet_file.read()
    tweet = json.loads(tweet_json)
    with open("./data/cities", 'r', encoding="utf-8") as city_file:
        known_locations += city_file.read().splitlines()
    with open('./data/us_state_codes', 'r', encoding="utf-8") as us_file:
        known_locations += us_file.read().splitlines()
    with open('./data/countries', 'r', encoding="utf-8") as country_file:
        known_locations += country_file.read().splitlines()
    for index, _ in enumerate(tweet):
        loc = tweet[index]["User-Location"]
        if loc == "" or loc is None:
            continue
        for line in known_locations:
            if line.strip() in loc:
                tweets_with_known_location.append(tweet[index])
                break
    print(f"Got {str(len(tweets_with_known_location))} tweets with known location")
    utils.write_to_json(filtered_file_name, tweets_with_known_location)
    return filtered_file_name


def _sentiment_analyis(tweet_text):
    """Perform sentiment analysis with TextBlob.
    https://planspace.org/20150607-textblob_sentiment/.
    """
    analysis = TextBlob(tweet_text)
    return analysis.sentiment


if __name__ == "__main__":
    file_name = str(sys.argv[1])
    output_csv = str(sys.argv[2])
    json_file = _filter_known_locations(file_name)
    all_tweets = []
    all_loc = []
    with open(file_name) as tweet_file:
        tweet_json = tweet_file.read()
    json_tweets = json.loads(tweet_json)
    for index, _ in enumerate(json_tweets):
        tweet_info = json_tweets[index]
        tweet_text = tweet_info['Text']
        tweet_loc = tweet_info["User-Location"]
        all_tweets.append((tweet_text, _sentiment_analyis(tweet_text)))
        all_loc.append(tweet_loc)

    _classifier(all_tweets, all_loc, output_csv)
