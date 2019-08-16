from flask import Flask, request, jsonify

from SummarizerPackage.SSummarizer import Summarizer
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
    return jsonify({"summary":summary})


@app.route('/getactions', methods=['POST'])
def getactions():
    req_data = request.get_json()
    print(req_data)
    transcript= req_data['content']
    obj = Summarizer()
    return jsonify(obj.extract_actions(transcript))

app.run()