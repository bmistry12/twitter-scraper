# Twitter Scraper

[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/bmistry12/twitter-scraper/?ref=repository-badge)


## Setup
Apply for a Twitter development account [here](https://developer.twitter.com/en/apply-for-access). Naturally you'll also need a twitter account.

## Setting Up Credentials - Hashicorp Vault :lock:
Install Hashicorp Vault (if not already done so)
</br> Various Download Links: 
> https://learn.hashicorp.com/vault/getting-started/install </br>
> https://www.vaultproject.io/downloads.html </br>
> https://chocolatey.org/packages/vault

Start up Vault Server
```
vault server -dev
```

Copy 
```
Unseal Key: xxx
Root Token: xxx
````

Open new terminal
```
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_DEV_ROOT_TOKEN_ID='xxx'
```

Check vault can be connected to & is running correctly
```
vault status
```

Put Secrets Into Vault
```
vault kv put secret/twitter consumer_key=<xxx> consumer_secret=<xxx> access_token=<xxx> access_token_secret=<xxx>
```

Get Secrets From Vault (sanity check)
```
vault kv get secret/twitter
vault kv get -field=consumer_key secret/twitter
```

### Being Uncool and Not Using Vault
This of course still runs without Vault.<br>
Comment out any references to `credentials.py` (e.g. in run.sh and as `import credentials`), and set the variables in `historic_twitter_data.__main__` manually.

## Run :running:

```
./run.sh "<keywords>" <number_of_tweets_to_fetch> <output_json_filename> <output_csv_for_data>
```
The only required argument is keywords, which can be a string of different words seperated by commas.

Or, if for some reason you don't like the existence of shell scripts:
```
pip install -r requirements.txt
py credentials.py
py historic_twitter.py <keywords> <output json file name>
py json_analysis.py <output json file name> <output csv for data>
py mapper.py <output csv name>
```

### This Code Sucks :nauseated_face:
See any issues or terrible code? Feel free to create an issue or PR to fix them.

To keep code consistent Flake8 should be used for linting checks.
`flake8 --max-line-length 100`
