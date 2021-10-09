import os
import hvac


class VaultError(Exception):
    """Vault Exception."""


class Credentials():
    """Get twitter developer credentials from Vault."""

    def __init__(self):
        self.consumer_key = ""
        self.consumer_secret = ""
        self.access_token = ""
        self.access_secret = ""
        self.run()

    def get_consumer_key(self):
        """Get consumer key."""
        if self.consumer_key == "":
            raise VaultError("Empty consumer key field")
        return self.consumer_key

    def get_consumer_secret(self):
        """Get consumer secret."""
        if self.consumer_secret == "":
            raise VaultError("Empty consumer secret field")
        return self.consumer_secret

    def get_access_token(self):
        """Get access token."""
        if self.access_token == "":
            raise VaultError("Empty access token field")
        return self.access_token

    def get_access_secret(self):
        """Get access token secret."""
        if self.access_secret == "":
            raise VaultError("Empty access token secret field")
        return self.access_secret

    def run(self):
        """Setup HVAC Client, and fetch secrets required to run the scripts.

        https://hvac.readthedocs.io/en/stable/overview.html#kv-secrets-engine-version-2
        """
        try:
            client = hvac.Client(
                url=os.environ["VAULT_ADDR"],
                token=os.environ["VAULT_DEV_ROOT_TOKEN_ID"]
            )
        except hvac.exceptions.VaultNotInitialized as error:
            raise VaultError(error)
        except hvac.exceptions.VaultDown as error:
            raise VaultError(error)
        except hvac.exceptions.Unauthorized as error:
            raise VaultError(error)
        except hvac.exceptions.VaultError as error:
            raise VaultError(error)
        except KeyError:
            raise VaultError(
                "Credentials aren't set - did you export them from the server?"
            )
        # Check if connected to vault
        if client.is_authenticated():
            read_response = client.secrets.kv.read_secret_version(path="twitter")
            self.consumer_key = ("{val}".format(
                val=read_response["data"]["data"]["consumer_key"]))
            self.consumer_secret = ("{val}".format(
                val=read_response["data"]["data"]["consumer_secret"]))
            self.access_token = ("{val}".format(
                val=read_response["data"]["data"]["access_token"]))
            self.access_secret = ("{val}".format(
                val=read_response["data"]["data"]["access_token_secret"]))
        else:
            raise VaultError(
                "ERROR - client not authenticated %s" % str(client.is_authenticated())
            )
