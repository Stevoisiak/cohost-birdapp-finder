import csv
import requests

# Check follows for a Twitter account and see if accounts with the same username exist on Cohost
# Retrieving twitter follows based on https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Follows-Lookup/following_lookup.py

def main():

    bearer_token = input("Enter twitter bearer token. (Obtained from https://developer.twitter.com/en)\nBearer Token: ")
    user_id = input("Enter your twitter account's user ID. (Obtained from https://tweeterid.com/)\nUser ID: ")
    url = f"https://api.twitter.com/2/users/{user_id}/following"
    params = {"max_results": 1000}
    headers = {"Authorization": f"Bearer {bearer_token}"}

    # Get follows list from Twitter
    # TODO: Limited to 1000 followers. Requires pagation support.
    #       https://developer.twitter.com/en/docs/twitter-api/pagination
    input("Press Enter to get Twitter follow list...")
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

    # Check each twitter username for a cohost account
    users = []
    for u in json_response["data"]:
        username = u['username']

        # Check if cohost account exists
        # print(f"Checking cohost for user {username}.")
        url = f'https://cohost.org/{username}'
        r = requests.head(url, timeout=10)
        if r.status_code == 200:
            user = {
                'twitter_id': u['id'],
                'twitter_display_name': u['name'],
                'twitter_username': u['username'],
                'cohost_url': url
            }
            users.append(user)
            print(u["name"] + " --> " + url)
        elif r.status_code == 404:
            # Cohost account does not exist
            pass
        else:
            raise Exception(
                "Cohost request returned an error: {} {}".format(
                    r.status_code, r.text
                )
            )

    # TODO: Error handling if writing to file fails
    print(f"Found {len(users)} Cohost accounts. Writing to file...")
    with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        csv_writer.writerow(['Twitter ID', 'Twitter Display Name', 'Username', 'Cohost URL'])
        for u in users:
            csv_writer.writerow([u['twitter_id'], u['twitter_display_name'], u['twitter_username'], u['cohost_url']])
    print("Finished saving to output.csv")

if __name__ == "__main__":
    main()
