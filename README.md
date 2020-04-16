# Twitter Scraper
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/bmistry12/twitter-scraper/?ref=repository-badge)

## Setup
Install python dependencies using one of the following:
- `python setup.py install` 
- `pip install -r requirements.txt`

**You are required to have a twitter developer accout to use this**

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

### Put Secrets Into Vault
```
vault kv put secret/twittertest consumer_key=xxx consumer_secret=xxxx access_token=xxx access_token_secret=xxx
```

### Get Secrets From Vault
```
vault kv get secret/twittertest
vault kv get -field=consumer_key secret/twittertest
```

## Run :running:
There are multiple options

1) Run via shell script
```
./run.sh "keywords" "output json file name" "output csv for data"
```

2) Run via python scripts
    ```
    py credentials.py
    py historic_twitter.py <keywords> <output json file name>
    py json_analysis.py <output json file name> <output csv for data>
    ```

    *Eventually this will be cleaned up and one main file will run everything*