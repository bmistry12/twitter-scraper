import sys  # noqa: E902
import tweepy
import credentials
import utils
from tweepy import API, OAuthHandler, TweepError


class HistoricTweetException(Exception):
    """Historic Twitter Data Exception."""
    pass


def _get_historic_tweets(api, keyword, json_file_name, num_of_tweets):
    """Get previous arg.num_of_tweets related to arg.keyword."""
    tweet_list = []
    print("Getting previous %s tweets..." % str(num_of_tweets))
    try:
        for tweet in tweepy.Cursor(api.search, q=keyword).items(num_of_tweets):
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
            tweet_list.append(entry)
        print("...tweets fetched")
        utils.write_to_json(json_file_name, tweet_list)
    except tweepy.TweepError as e:
        raise HistoricTweetException(str(e))


if __name__ == "__main__":
    arg_keyword = "".join(sys.argv[1])
    arg_num_of_tweets = int(sys.argv[2])
    arg_json_file_name = sys.argv[3]
    # Get credentials
    try:
        consumer_key = credentials.get_consumer_key()
        consumer_secret = credentials.get_consumer_secret()
        access_token = credentials.get_access_token()
        access_token_secret = credentials.get_access_secret()
    except credentials.VaultException as error:
        raise HistoricTweetException("Vault Exception: " + str(error))
    # Set Up Auth
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth)
    except TweepError as err:
        raise TweepError("Authentication Failed: " + str(err))

    _get_historic_tweets(
        api, arg_keyword, arg_json_file_name, arg_num_of_tweets
    )
