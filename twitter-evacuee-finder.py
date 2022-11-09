import requests

# Retrieving twitter follows based on https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Follows-Lookup/following_lookup.py

def main():
    # Get list of twitter follows for a user then check if accounts exist on Cohost 

    # https://developer.twitter.com/en
    bearer_token = input("Enter twitter bearer token. (Obtained from https://developer.twitter.com/en)\nBearer Token: ")
    user_id = input("Enter your twitter account's user ID. (Obtained from https://tweeterid.com/)\nUser ID: ")
    url = f"https://api.twitter.com/2/users/{user_id}/following"
    params = {"max_results": 1000}
    headers = {"Authorization": f"Bearer {bearer_token}"}

    # Get follows list from Twitter
    # TODO: Limited to 1000 followers. Requires pagation support.
    #       https://developer.twitter.com/en/docs/twitter-api/pagination
    input(f"Press Enter to get Twitter follow list for {user_id}...")
    r = requests.get(url, params=params, headers=headers, timeout=10)
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
        url = f'https://cohost.org/{username}'
        r = requests.head(url, timeout=10)
        if r.status_code == 200:
            print(u["name"] + " --> " + url)
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
