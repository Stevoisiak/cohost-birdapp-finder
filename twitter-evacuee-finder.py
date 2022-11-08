import requests
import json
import keyring
import logging

# Retrieving twitter follows based on https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Follows-Lookup/following_lookup.py

# Get bearer token
bearer_token = keyring.get_password("twitter_evacuee_finder", "bearer_token")

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowingLookupPython"
    return r


def connect_to_endpoint(url: str, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    # Get Twitter following list
    twitter_user_id = 92179256  # Stevoisiak
    twitter_url = f"https://api.twitter.com/2/users/{twitter_user_id}/following"


    # TODO: Get more than the first 100 follows
    logging.info(f"Retrieving followed users for Twitter user {twitter_user_id} ")
    json_response = connect_to_endpoint(twitter_url, None)
    print(json.dumps(json_response, indent=4, sort_keys=True))

    user_list = {}

    # Iterate through twitter users
    for followed_user in json_response["data"]:
        followed_username = followed_user["username"]

        # Check if cohost URL exists
        cohost_url = f'https://cohost.org/{followed_username}'
        r = requests.get(cohost_url)
        if r.status_code == 200:
            print(cohost_url)


if __name__ == "__main__":
    main()





"""
from requests_oauthlib import OAuth1Session
import keyring

# Based on https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_user_context.py

# Get API keys from environment variables
consumer_api_key = keyring.get_password("twitter_evacuee_finder", "api_key")
consumer_secret = keyring.get_password("twitter_evacuee_finder", "api_key_secret")


# Get request token from Twitter
request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_api_key, client_secret=consumer_secret)
try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print("Could not fetch oauth response.")
resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)


# Get authorization to acess twitter account
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_api_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_api_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)
response = oauth.get(
    "https://api.twitter.com/2/users/by",
)

if response.status_code != 200:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print(response)
"""