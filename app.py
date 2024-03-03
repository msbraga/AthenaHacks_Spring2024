from flask import Flask, render_template
import requests
import json
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import wave
import shutil




app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'audio')

API_TOKEN = "US_LOl-j5qoeGNOPOb4Et54RF6Ysc3i_COv1RP9m"
ACCOUNT_ID = "e400b2d016c3520024ca92809e6e9f4d"



def split_wav(input_file, output_dir, chunk_length_seconds):
    """Splits a WAV file into chunks of a specified length in seconds.

    Args:
        input_file: The path to the input WAV file.
        output_dir: The path to the output directory where the chunks will be saved.
        chunk_length_seconds: The length of each chunk in seconds.
    """

    # Create the output directory if it doesn't exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the input WAV file.
    with wave.open(input_file, "rb") as input_file:
        # Get the number of frames in the file.
        num_frames = input_file.getnframes()
        frame_rate = input_file.getframerate()

        # Calculate the number of chunks.
        num_chunks = num_frames // (frame_rate * chunk_length_seconds)
        remainder_frames = num_frames % (frame_rate * chunk_length_seconds)

        # Split the file into chunks.
        for i in range(num_chunks):
            # Calculate the start and end frames for the chunk.
            start_frame = i * (frame_rate * chunk_length_seconds)
            end_frame = (i + 1) * (frame_rate * chunk_length_seconds)

            # Open the output file.
            output_file_path = os.path.join(output_dir, f"{i}.wav")
            with wave.open(output_file_path, "wb") as output_file:
                # Set the parameters of the output file.
                output_file.setparams(input_file.getparams())

                # Write the chunk to the output file.
                output_file.writeframes(input_file.readframes(end_frame - start_frame))

        # Process the remainder frames for the last chunk.
        if remainder_frames > 0:
            start_frame = num_chunks * (frame_rate * chunk_length_seconds)
            end_frame = num_frames
            output_file_path = os.path.join(output_dir, f"{num_chunks}.wav")
            with wave.open(output_file_path, "wb") as output_file:
                output_file.setparams(input_file.getparams())
                output_file.writeframes(input_file.readframes(end_frame - start_frame))

class UploadForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")    


@app.route("/")
def home():    
    return render_template("website_main.html")

@app.route("/record-button", methods=["GET", "POST"])
def record_button():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        transcript = get_text(file.filename)
        summary = summarize_with_gpt(transcript)
        return render_template("output.html", transcript = transcript, summary = summary)

    return render_template("InsertFile_Page.html", form = form)


def get_text(filename):
    #first let's send a request with our sound file to the API

    split_wav("./audio/"+filename, "output_dir", 30)

    string = ""

    for i in range(100):
        filepath = os.path.join("output_dir", f"{i}.wav")
        if os.path.isfile(filepath):

            url = "https://api.cloudflare.com/client/v4/accounts/" + ACCOUNT_ID +"/ai/run/@cf/openai/whisper"


            with open(filepath, 'rb') as f:
                payload = f.read()

            headers = {
                "Content-Type": "application/octet-stream",
                "Authorization": "Bearer " + API_TOKEN
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            print("response status code" + str(response.status_code))

            data = json.loads(response.text)

            #print(data['result']['text'])
            if (response.status_code == 200):
                string += data['result']['text'] + " "

        
    
    shutil.rmtree("output_dir")
    return string

  


def summarize_text(string):
    #now lets have the API summarize our text

    url = "https://api.cloudflare.com/client/v4/accounts/"+ ACCOUNT_ID +"/ai/run/@cf/facebook/bart-large-cnn"

    payload = {
        "input_text": "\""+ string + "\"",
        "max_length": 250
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_TOKEN
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = json.loads(response.text)


    return data['result']['summary']



def summarize_with_gpt(string):
    url = "https://api.cloudflare.com/client/v4/accounts/"+ ACCOUNT_ID +"/ai/run/@cf/openchat/openchat-3.5-0106"

    payload = {
        "max_tokens": 256,
        "prompt": "\""+ "Please summarize the following:"+ string + "\"",
        "raw": False,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_TOKEN
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    data = json.loads(response.text)


    return data['result']['response']


if __name__ == "__main__":
    app.run()