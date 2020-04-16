import os
import hvac

# https://hvac.readthedocs.io/en/stable/overview.html#kv-secrets-engine-version-2

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Set up new hashicorp vault client
client = hvac.Client()
# variables must be exported before hand - from the running Vault server
client = hvac.Client(
 url=os.environ['VAULT_ADDR'],
 token=os.environ['VAULT_DEV_ROOT_TOKEN_ID']
)
# Check connected to vault
print(client.is_authenticated())

if client.is_authenticated():
    read_response = client.secrets.kv.read_secret_version(path='twittertest')
    print(read_response)
    consumer_key = ('{val}'.format(val=read_response['data']['data']['consumer_key']))
    consumer_secret = ('{val}'.format(val=read_response['data']['data']['consumer_secret']))
    access_token = ('{val}'.format(val=read_response['data']['data']['access_token']))
    access_token_secret = ('{val}'.format(val=read_response['data']['data']['access_token_secret']))
else :
    print("ERROR - client not authenticated")

def getConsumerKey():
    if consumer_key == '':
        print("Empty consumer key field")
    return consumer_key

def getConsumerSecret():
    if consumer_secret == '':
        print("Empty consumer secret field")
    return consumer_secret

def getAccessToken():
    if access_token == '':
        print("Empty access token field")
    return access_token
    
def getAccessTokenSecret():
    if access_token_secret == '':
        print("Empty access token secret field")
    return access_token_secret