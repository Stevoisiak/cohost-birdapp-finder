# cohost-birdapp-finder
Retrieves users you follow on Twitter and checks if accounts with the same usernames exist on Cohost.

## How to use

Before using you will need to get a bearer token from [Twitter's Developer Platform](https://developer.twitter.com/en).

1. Run `cohost-birdapp-finder.py`
2. Input your bearer token and hit Enter.
3. Input your Twitter username (without the @) and hit Enter.
4. Hit Enter to confirm your display name is correct.
5. Wait for program to finish. Results will be output to `output.csv`.

## Limitations
- Only retrieves your most 1000 most recent follows
- Minimal error handling
- Requires a twitter bearer token

This was written in 3 days primarilly for personal use. Ideally this would be a webapp so you don't need to download and locally run Python code.
