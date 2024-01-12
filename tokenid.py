import requests
from dotenv import load_dotenv, set_key
import os
import urllib.parse

# Load the .env file
load_dotenv()

# Your LinkedIn credentials
client_id = os.getenv('LINKEDIN_CLIENT_ID')
client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
redirect_uri = urllib.parse.quote('https://www.linkedin.com/developers/tools/oauth/redirect')
authorization_url = 'https://www.linkedin.com/oauth/v2/authorization'



# Construct the authorization URL
scope = 'openid%20profile%20email%20w_member_social'  # Encoded with %20 instead of spaces
full_auth_url = f"{authorization_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
print("Go to this URL to authorize:", full_auth_url)

# Exchange the authorization code for an access token
authorization_code = input("Enter the authorization code: ")
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
payload = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': urllib.parse.unquote(redirect_uri),
    'client_id': client_id,
    'client_secret': client_secret
}
response = requests.post(token_url, data=payload)

if response.status_code == 200:
    access_token = response.json().get('access_token')
    print("Access Token:", access_token)

    # Update the .env file with the Access Token
    set_key('.env', 'LINKEDIN_ACCESS_TOKEN', access_token)
    print(".env file updated with LinkedIn Access Token.")

    # Use the access token to get user information from the userinfo endpoint
    userinfo_url = 'https://api.linkedin.com/v2/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    userinfo_response = requests.get(userinfo_url, headers=headers)

    if userinfo_response.status_code == 200:
        userinfo_data = userinfo_response.json()
        linkedin_sub = userinfo_data.get('sub')  # This is the LinkedIn User ID (sub field)
        print("LinkedIn User ID (sub):", linkedin_sub)

        # Update the .env file with the LinkedIn User ID (sub) in the format 'urn:li:person:AUTHORCODE'
        linkedin_author_urn = f'urn:li:person:{linkedin_sub}'
        set_key('.env', 'LINKEDIN_AUTHOR', linkedin_author_urn)
        print(".env file updated with LinkedIn User ID (sub).")
    else:
        print("Failed to retrieve LinkedIn User ID (sub). Error:", userinfo_response.text)
else:
    print("Failed to retrieve Access Token. Error:", response.text)
