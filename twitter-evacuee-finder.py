import requests
import json
import keyring
import logging

# Retrieving twitter follows based on https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Follows-Lookup/following_lookup.py

# Get bearer token
twitter_bearer_token = keyring.get_password("twitter_evacuee_finder", "bearer_token")


def main():
    # Get list of twitter follows for a user then check if accounts exist on Cohost 

    twitter_user_id = 92179256  # Stevoisiak
    twitter_url = f"https://api.twitter.com/2/users/{twitter_user_id}/following"
    twitter_headers = {
        "Authorization": f"Bearer {twitter_bearer_token}"
    }

    # Get follows list from Twitter
    # TODO: Get more than the first 100 follows
    response = requests.get(twitter_url, headers=twitter_headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))


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
