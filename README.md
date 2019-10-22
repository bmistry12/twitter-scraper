# Twitter Scraper

## Setup
Install python dependencies using one of the following:
- `python setup.py install` 
- `pip install -r requirements.txt`

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
./run.sh "keywords" "output json file name"
```

2) Run via python scripts
    ```
    py credentials.py
    py historic_twitter.py <keywords> <output json file name>
    py json_analysis.py <output json file name>
    ```

    *Eventually this will be cleaned up and one main file will run everything*