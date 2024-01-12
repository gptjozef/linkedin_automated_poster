hey thanks for checking out my repo, follow me on X for great content, tips, and more code: [Twitter](https://twitter.com/gptjozef)

going to lay it out step by step what you need to get before you can get started 

What you need: 

A code editor (IDE), either vs code, or cursor will work.

The following dependencies:

* requests - pip install requests
* openai - pip install openai
* schedule - pip install schedule
* dotenv (for load_dotenv and set_key) - pip install python-dotenv

First stage is setting up all the environment variables which you will need to get, if you need any assistance, watch the following video: [Video](https://youtu.be/zeyNbxCkhIM)

step one you are going to need to set up a linkedin dev account, simple, easy, and free to do:

https://developer.linkedin.com/

Click "Create App"

![brave_mLivOf3KqT](https://github.com/gptjozef/linkedin_automated_poster/assets/112521836/89819d0c-f027-4925-856b-12cf7344e9b0)

Fill in the details, it really doesn't matter what you put here. Even though its asking for a linkedin page, you don't really need one, fill this out with whatever you need to do to get to the next step:

![image](https://github.com/gptjozef/linkedin_automated_poster/assets/112521836/180a73bc-d6b0-4106-aaed-e7ef78920177)

Next you will select "request access" on the Share on Linkedin, and Sign in with LinkedIn uising OpenID Connect products

![linkedin](https://github.com/gptjozef/linkedin_automated_poster/assets/112521836/9a481a64-09b0-403b-98ce-88a63b6a69fc)

The next step is to get the proper scopes in your app, at first you will see nothing:

![image](https://github.com/gptjozef/linkedin_automated_poster/assets/112521836/b4a2f3f3-10d2-471a-ab21-e8c312385f63)

First add the following as an authorized redirect URL: https://www.linkedin.com/developers/tools/oauth/redirect

![image](https://github.com/gptjozef/linkedin_automated_poster/assets/112521836/3287b47e-c874-46af-bef8-a10a7dd440c6)

To get the scripts you have to go to the following URL: https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https%3A%2F%2Fwww.linkedin.com%2Fdevelopers%2Ftools%2Foauth%2Fredirect&scope=openid%20profile%20email%20w_member_social

When you go that link you will need to authenticate yourself. Use your username and password to login. After authenticating, grab the entire URL that looks something like this:

![image](https://github.com/gptjozef/linkedin_automated_poster/assets/112521836/5dd7cc4f-6bc4-45e7-80e6-95e6a68bb995)

These tokens last for 60 days, after 60 days you will need to grab a new token. You can also refresh tokens, see the following documentation on how to do that, for now I haven't gone donw that rabbit hole. https://learn.microsoft.com/en-us/linkedin/shared/authentication/programmatic-refresh-tokens

Now notice all your scopes are going to be enabled on the auth tab. Make sure you have w_member_social enabled, or this won't work. 

![scope](https://github.com/gptjozef/linkedin_automated_poster/assets/112521836/8e418e41-a4c7-4a02-8147-fb7e9dd8c198)

Okay now that we got all of that out the way we are ready to start launching some code. First you will need to provide your OpenAI api key to the .env file, you can do research on how to get one but its super easy.

Next start the tokenid.py, command is pythong tokenid.py, click the link you are given and copy the code you receive in your url, paste it into your ide. This will get you your access token and your author id. That's it now you're ready to post. 

All you have to do from there is start the poster.py (python poster.py). I included two additional files, a scheduler.json and topics.json. You can adjust your scheduler, right now it works from EST 00:00-24:00. You can also edit your topics that your bot will talk about, I included examples from both and you should be able to derive the answers from either. 

If you need quick advice hit me up on X: [Twitter](https://twitter.com/gptjozef) That should be everything, thanks for following along!

File Contents: 

* poster.py — This will take all the other files and do the heavy lifting.
* tokenid.py — This gets your access token and author id
* .env — This is where all your important codes and tokens are
* scheduler.json — This is where you will put how many posts you want to schedule 
* topics — This is where you can set the topics to post about on your linkedin
