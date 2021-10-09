import sys  # noqa: E902
import utils
import tweepy
from credentials import Credentials, VaultError
from tweepy import API, OAuthHandler, TweepError


class HistoricTweetError(Exception):
    """Historic Twitter Data Exception."""
    pass


def _get_historic_tweets(api, keyword, json_file_name, num_of_tweets):
    """Get previous arg.num_of_tweets related to arg.keyword."""
    tweet_list = []
    print(f"Getting previous {str(num_of_tweets)} tweets...")
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
        raise HistoricTweetError(str(e))


if __name__ == "__main__":
    arg_keyword = "".join(sys.argv[1])
    arg_num_of_tweets = int(sys.argv[2])
    arg_json_file_name = sys.argv[3]
    # Get credentials
    vault_creds = Credentials()
    try:
        consumer_key = vault_creds.get_consumer_key()
        consumer_secret = vault_creds.get_consumer_secret()
        access_token = vault_creds.get_access_token()
        access_token_secret = vault_creds.get_access_secret()
    except VaultError as error:
        raise HistoricTweetError("Vault Exception: " + str(error))
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
