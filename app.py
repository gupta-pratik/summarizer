from flask import Flask, request, jsonify

from Summarizer.Summarizer import Summarizer
import os

app = Flask(__name__)
app.config["DEBUG"] = True

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=['GET'])
def home():
    return "<h1>Virtual Meeting Assistance</h1><p>Welcome to virtual meeting assistance</p>"

@app.route('/summary', methods=['POST'])
def getsummary():
    req_data = request.get_json()
    transcript= req_data['content']
    obj = Summarizer()
    summary = obj.getsummary(transcript)
    return summary


app.run()