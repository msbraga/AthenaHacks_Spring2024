# AthenaHacks_Spring2024

## Setup CloudFlare

Step 1
Create a CloudFlare account

Step 2
Once logged in, create an API token via the instructions in this link https://dash.cloudflare.com/e400b2d016c3520024ca92809e6e9f4d/ai/workers-ai/api-quick-start. Paste this value into app.py where it says API_TOKEN = "YOUR TOKEN HERE"

Step 3
Navigate to Account Home (the screen you see after you login) and then Workers, then on the right hand side, copy your account ID. Paste this value into app.py where it says ACCOUNT_ID = "YOUR ACCOUNT ID HERE"

## Setup your environment
Step 1
Open the Terminal on Visual Studio Code

Step 2
run the command:
pip install -r requirements.txt 
to make sure all requirements are downloaded with the correct minimum version

Step 3
run the command:
python app.py or python3 app.py

Step 4
This will generate a line that says "Running on" and then an http link. Click on that link or copy and paste it to your browser of choice.

Step 5
Enjoy Recapify!
