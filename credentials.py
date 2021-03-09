import os
import hvac


class VaultException(Exception):
    """Vault Exception."""
    pass


CONSUMER_KEY = CONSUMER_SECRET = ACCESS_TOKE = ACCESS_SECRET = ""


def get_consumer_key():
    """Get consumer key."""
    if CONSUMER_KEY == "":
        raise VaultException("Empty consumer key field")
    return CONSUMER_KEY


def get_consumer_secret():
    """Get consumer secret."""
    if CONSUMER_SECRET == "":
        raise VaultException("Empty consumer secret field")
    return CONSUMER_SECRET


def get_access_token():
    """Get access token."""
    if ACCESS_TOKEN == "":
        raise VaultException("Empty access token field")
    return ACCESS_TOKEN


def get_access_secret():
    """Get access token secret."""
    if ACCESS_SECRET == "":
        raise VaultException("Empty access token secret field")
    return ACCESS_SECRET


if __name__ == "__main__":
    """Setup HVAC Client, and fetch secrets required to run the scripts.

    https://hvac.readthedocs.io/en/stable/overview.html#kv-secrets-engine-version-2
    """
    try:
        client = hvac.Client(
            url=os.environ["VAULT_ADDR"],
            token=os.environ["VAULT_DEV_ROOT_TOKEN_ID"]
        )
    except hvac.exceptions.VaultNotInitialized as error:
        raise VaultException(error)
    except hvac.exceptions.VaultDown as error:
        raise VaultException(error)
    except hvac.exceptions.Unauthorized as error:
        raise VaultException(error)
    except hvac.exceptions.VaultError as error:
        raise VaultException(error)
    except KeyError:
        raise VaultException(
            "Credentials aren't set - did you export them from the server?"
        )
    # Check connected to vault
    if client.is_authenticated():
        read_response = client.secrets.kv.read_secret_version(path="twitter")
        print(read_response)
        CONSUMER_KEY = ("{val}".format(
            val=read_response["data"]["data"]["consumer_key"]))
        CONSUMER_SECRET = ("{val}".format(
            val=read_response["data"]["data"]["consumer_secret"]))
        ACCESS_TOKEN = ("{val}".format(
            val=read_response["data"]["data"]["access_token"]))
        ACCESS_SECRET = ("{val}".format(
            val=read_response["data"]["data"]["access_secret"]))
    else:
        raise VaultException("ERROR - client not authenticated %s" %
                             str(client.is_authenticated()))
