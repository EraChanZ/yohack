from flask import Flask
from flask import request, jsonify, render_template, redirect, url_for
import requests
import json

clientID = "fbqObFgAQ9mHmbsSCxFd1w"
clientSecret = "OsyFiv0UHHtfXDWX6Vn0ggULkAMmUN11"
redirectURL = "https://eeb987f9.ngrok.io"
userSessions = {}

app = Flask(__name__)

users = []

@app.route('/', methods=['GET'])
def main():
    global userSessions
    active = False
    username = request.args.get('username')
    users.append({'username': username})
    if request.args.get('active'): active = True
    if request.args.get('code'):
        print(request.args.get('code'))
        url = 'https://zoom.us/oauth/token?grant_type=authorization_code&code=' + request.args.get(
            'code') + '&redirect_uri=' + redirectURL
        res = requests.post(url, data={'client_id': clientID, 'client_secret': clientSecret})
        res = json.loads(res.text)
        print(res)
        if ('access_token' in res):
            token = res['access_token']
            token_ref = res['refresh_token']
            userSessions[clientID] = {'token': token, 'token_ref': token_ref}
            print(userSessions[clientID], 'i am here')
    if active:
        return render_template("index.html", username=users)
    else:
        return "Конференция не началась"


@app.route('/developmentnotification', methods=['POST'])
def developmentnotification():
    data = request.json
    if 'event' in data:
        if data['event'] == 'meeting.started':
            return redirect('/?active=True')
        elif data['event'] == 'meeting.participant_joined':
            return redirect(url_for('/', username=data['payload']['object']['participant']['user_name'], active = True))
    return "..."


@app.route('/livestream', methods=['POST'])
def livestream():
    print(request.json)
    return "5A6XsoFmQByZtMe-Z9jbyQ"


@app.route('/livestream/123', methods=['POST'])
def livestream123():
    print(request.json)
    return "5A6XsoFmQByZtMe-Z9jbyQ"


@app.route('/productionnotification', methods=['POST'])
def productionnotification():
    data = request.json
    print(data, 'hello')
    return "5A6XsoFmQByZtMe-Z9jbyQ"


app.run(port=4000)
