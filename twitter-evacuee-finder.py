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
    twitter_headers = {"Authorization": f"Bearer {twitter_bearer_token}"}

    # Get follows list from Twitter
    # TODO: Get more than the first 100 follows
    r = requests.get(twitter_url, headers=twitter_headers)
    if r.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                r.status_code, r.text
            )
        )
    json_response = r.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

    users = []
    # Iterate through twitter users
    for u in json_response["data"]:
        username = u['username']

        # Check if cohost account exists
        print(f"Checking cohost for user {username}.")
        request_url = f'https://cohost.org/{username}'
        r = requests.get(request_url)
        if r.status_code == 200:
            # TODO: Get more inforation about user
            print("Cohost account found")
            user = {
                'twitter_id': u['id'],
                'twitter_display_name': u['name'],
                'twitter_username': u['username'],
                'cohost_username': u['username']
            }
            users.append(user)
        elif r.status_code == 404:
            print("Cohost account does not exist (404)")
        else:
            raise Exception(
                "Cohost request returned an error: {} {}".format(
                    r.status_code, r.text
                )
            )

if __name__ == "__main__":
    main()
