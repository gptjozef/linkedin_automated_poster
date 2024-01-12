import requests
from urllib.parse import urlencode, parse_qs, urlsplit
import openai
import time
import os
import json
import random
import schedule
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# LinkedIn OAuth 2.0 settings
client_id = os.getenv('LINKEDIN_CLIENT_ID')
client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
linkedin_access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
linkedin_author = os.getenv('LINKEDIN_AUTHOR')


# OpenAI API Key
openai_api_key = os.getenv('OPENAI_API_KEY')


# Load topics from JSON file
with open('topics.json', 'r') as file:
    topics_data = json.load(file)
topics = topics_data['topics']


# Check for existing access token
def check_for_existing_token():
    # Check if token is available in .env file
    if linkedin_access_token:
        return linkedin_access_token


# Function to generate post content using GPT-3.5 Chat
def generate_post_content():
    openai.api_key = openai_api_key
    # A random topic is chosen from the topics.json
    randomTopic = random.choice(topics)
    # A random amount of words in chosen for each post, you can edit this however you want, it is between 10 - 250 words, with a floor of 10 words meaning it can only select 10,20 etc. not 11,16,25, etc.
    wordsAmount = random.choice(range(10, 251, 10))
    print(f"Generating post content about {randomTopic}...")
    # This is where the post content is generated
    response = openai.ChatCompletion.create(
        # This is the most up to date GPT4 model, you can switch to gpt-3.5-turbo to save money.
        model="gpt-4-1106-preview",
        messages=[
        # Keep the system message constant
        {"role": "system", "content": "You are a helpful assistant."},
        # Here you can customize the prompt to the AI model. We grab the random words amount and the topic to be used to create a post. You can edit as you see fit, but don't bug me if you break the script. 
        {"role": "user", "content": f"In {wordsAmount} words, and without using any hashtags or emojis, write a post that seems as human written as possible and emulate a guru type post about: {randomTopic}."}
        ]
        )
    return response['choices'][0]['message']['content'].strip()

# Function to post to LinkedIn
def post_to_linkedin():
    access_token = check_for_existing_token()
    if not access_token:
        print("Access token not found. Please authorize.")
        return
    linkedin_author
    post_content = generate_post_content()
    post_data = {
        "author": linkedin_author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f"{post_content}"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    post_response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=post_data)
    post_response.raise_for_status()
    print("Post successfully created with ID:", post_response.json().get('id'))



# Function to dynamically set up schedule
# Scheduler.json is in EST 00:00:00-24:00:00 format
def setup_schedule():
    with open('scheduler.json', 'r') as file:
        schedules = json.load(file)
    for item in schedules:
        time = item['time']
        function_name = item['function']
        if function_name == 'post_to_linkedin':
            schedule.every().day.at(time).do(post_to_linkedin)

# If you want to see if the bot works, remove the below # and it will post to linkedin as soon as you run the script.             
#post_to_linkedin()


# Main process
if __name__ == "__main__":
    setup_schedule()
    while True:
        schedule.run_pending()
        time.sleep(1)
