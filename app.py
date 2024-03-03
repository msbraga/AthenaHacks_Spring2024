from flask import Flask, render_template
import requests
import json
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


app = Flask(__name__)

API_TOKEN = "US_LOl-j5qoeGNOPOb4Et54RF6Ysc3i_COv1RP9m"
ACCOUNT_ID = "e400b2d016c3520024ca92809e6e9f4d"

class UploadForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Submit")    


@app.route("/")
def home():    
    return render_template("website_main.html")

@app.route("/record-button")
def record_button():
    return render_template("InsertFile_Page.html")


def get_text():
    #first let's send a request with our sound file to the API

    url = "https://api.cloudflare.com/client/v4/accounts/" + ACCOUNT_ID +"/ai/run/@cf/openai/whisper"

    with open('c.wav', 'rb') as f:
        payload = f.read()

    headers = {
        "Content-Type": "application/octet-stream",
        "Authorization": "Bearer " + API_TOKEN
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    data = json.loads(response.text)

    print(data['result']['text'])

    string = data['result']['text']


def summarize_text(string):
    #now lets have the API summarize our text

    url = "https://api.cloudflare.com/client/v4/accounts/"+ ACCOUNT_ID +"/ai/run/@cf/facebook/bart-large-cnn"

    payload = {
        "input_text": "\""+ string + "\"",
        "max_length": 1024
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_TOKEN
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)


if __name__ == "__main__":
    app.run()