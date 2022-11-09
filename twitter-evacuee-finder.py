import requests

# Retrieving twitter follows based on https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Follows-Lookup/following_lookup.py

def main():
    # Get list of twitter follows for a user then check if accounts exist on Cohost 

    # https://developer.twitter.com/en
    twitter_bearer_token = input("Enter twitter bearer token. (Obtained from https://developer.twitter.com/en)\nBearer Token: ")
    twitter_user_id = input("Enter your twitter account's user ID. (Obtained from https://tweeterid.com/)\nUser ID: ")
    twitter_url = f"https://api.twitter.com/2/users/{twitter_user_id}/following"
    twitter_params = {"max_results": 1000}
    twitter_headers = {"Authorization": f"Bearer {twitter_bearer_token}"}

    # Get follows list from Twitter
    # TODO: Limited to 1000 followers. Requires pagation support.
    #       https://developer.twitter.com/en/docs/twitter-api/pagination
    input(f"Press Enter to get Twitter follow list for {twitter_user_id}...")
    r = requests.get(twitter_url, params=twitter_params, headers=twitter_headers, timeout=10)
    if r.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                r.status_code, r.text
            )
        )
    json_response = r.json()
    print(f"Retrieved {json_response['meta']['result_count']} follows")
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    # Iterate through twitter users
    input(f"Press Enter to check for cohost accounts...")
    for u in json_response["data"]:
        username = u['username']

        # Check if cohost account exists
        # print(f"Checking cohost for user {username}.")
        request_url = f'https://cohost.org/{username}'
        r = requests.head(request_url, timeout=10)
        if r.status_code == 200:
            print(u["name"] + " --> " + request_url)
        elif r.status_code == 404:
            pass
            # print("Cohost account does not exist (404)")
        else:
            raise Exception(
                "Cohost request returned an error: {} {}".format(
                    r.status_code, r.text
                )
            )

if __name__ == "__main__":
    main()
