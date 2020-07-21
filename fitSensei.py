from flask import Flask, request
import requests
import sys
import os
import json
from Credentials import *

app = Flask(__name__)
GREETINGS = ['hi', 'hello', 'howdy', 'hey']

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        return request.args.get('hub.challenge', 200)
    else:
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    log(data)
    bot_id = data["entry"][0]["id"]
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    if(sender_id != bot_id):
                        recipient_id = messaging_event["recipient"]["id"]
                        message_text = messaging_event["message"]["text"]
                        userinfo = json.loads(getFirstName(sender_id))
                        response = 'Sorry, I do not understand that as yet'
                        if message_text in GREETINGS:
                            response = 'Nǐ hǎo ' +userinfo.get("first_name")+ ', Welcome to Fit Sensei, what would you like to do?' 
                            send_quickreply(sender_id, response)
                        elif message_text == "Reach your goals":
                            response = "You selected reach your goals"
                            send_message(sender_id, response)
                        elif message_text == "Track my progress":
                            response = "You selected track your progress"
                            send_message(sender_id, response)
                        elif message_text == "Find an exercise":
                            response = "You selected find an exercise"
                            send_message(sender_id, response)
                        else:
                            send_message(sender_id, response)
                if messaging_event.get("delivery"):
                    pass

                if messaging_event.get("optin"):
                    pass

                if messaging_event.get("postback"):
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)

def send_quickreply(recipient_id, message_text):
    
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": message_text,
            "quick_replies": [
                {
                   "content_type": "text",
                   "title": "Reach your goals",
                   "payload": "POSTBACK_GOALS",
                },
                {
                    "content_type": "text",
                    "title": "Find an Exercise",
                    "payload": "POSTBACK_FINDEX",
                },
                {
                    "content_type": "text",
                    "title": "Track my progress",
                    "payload": "POSTBACK_TRACKP",
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)

@app.route('/', methods=['GET'])
def getFirstName(sender_id):
    
    params = {
        ("fields", "first_name"),
        ("access_token", PAGE_ACCESS_TOKEN)
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.get("https://graph.facebook.com/"+sender_id, params=params, headers=headers)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)
    return r.text
    
def log(message):  # simple wrapper for logging to stdout on heroku
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    app.run(debug = True, port= 80)
