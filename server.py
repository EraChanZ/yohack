from flask import Flask
from flask import request, jsonify
import requests
import json


clientID="fbqObFgAQ9mHmbsSCxFd1w"
clientSecret="OsyFiv0UHHtfXDWX6Vn0ggULkAMmUN11"
redirectURL="https://eeb987f9.ngrok.io"
userSessions = {}

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    global userSessions
    if request.args.get('code'):
        print(request.args.get('code'))
        url = 'https://zoom.us/oauth/token?grant_type=authorization_code&code=' + request.args.get('code') + '&redirect_uri=' + redirectURL
        res = requests.post(url, data = {'client_id':clientID, 'client_secret':clientSecret})
        res = json.loads(res.text)
        print(res)
        if ('access_token' in res):
            token = res['access_token']
            token_ref = res['refresh_token']
            userSessions[clientID] = {'token':token, 'token_ref':token_ref}
            print(userSessions[clientID], 'i am here')
    return "something"
    

@app.route('/developmentnotification', methods=['POST'])
def developmentnotification():
    data = request.json
    if 'event' in data:
        if data['event'] == 'meeting.started':
            try:
                meetingId = data['payload']['object']['id']
            except:
                meetingId = ''
            if meetingId:
                url = "https://api.zoom.us/v2/meetings/{}/livestream/status".format(str(meetingId))
                #data = {'access_token':userSessions[clientID]['token']},
                res = requests.patch(url, json = { "stream_url": redirectURL+"/livestream","stream_key": "secret","page_url": redirectURL+"/livestream/123"} ,data = {'access_token':userSessions[clientID]['token']},headers = {'Content-Type':'application/json', 'Authorization':'Bearer '+ userSessions[clientID]['token']})
                res = res.text
                print(res)
    return "5A6XsoFmQByZtMe-Z9jbyQ"

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