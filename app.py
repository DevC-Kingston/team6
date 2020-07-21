import os, sys
from flask import Flask, request
from pymessenger import Bot
import requests
import json

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAJTDsRU4kkBAIZClO4C1KPyLIL68ZCXA4HqZCTv1RTCUZABLZAzY2JEtDoZAZAWRsgScp0bsLzZBJobfXvzrNrHda3NjfI9toWjlqHtAS7GRNlakJxi156qkFwx4Id4ozC6lNC41H4rZBIL0F0zdxdAaN3ZBBhmc0g5mkRa8rSlJeZCw5WFPnMLn8r'

bot = Bot(PAGE_ACCESS_TOKEN)
GREETINGS = ['is anyone available to chat?', 'wah gwaan', 'sup','hey','hi','yo','hello','good afternoon']
POUNDS = ['5','10','20','30','40','more']
BODY = ['core','upper','lower']


def core(level,sender):
    revCrunches = 10 * level
    alternatingCurls = 10 * level
    legRaise = 10 * level
    bot.send_text_message(sender, "You're new so These Exercises are a good start")
    bot.send_text_message(sender, "Remember no breaks")
    advice = "You should do "+str(revCrunches)+" Reverse Crunches\n"+str(alternatingCurls)+" Alternating Curls"
    bot.send_text_message(sender, advice)
    bot.send_text_message(sender, "And "+str(legRaise)+" Leg Raises")

def upper(level,sender):
    Pushup = 10 * level
    BenchPush = 10 * level
    InOutPush = 10 * level
    bot.send_text_message(sender, "You're new so These Exercises are a good start")
    bot.send_text_message(sender, "Remember no breaks")
    advice = "You should do " + str(Pushup) + " Push Ups\n" + str(BenchPush) + " Foot on Bench Push Ups"
    bot.send_text_message(sender, advice)
    bot.send_text_message(sender, "And " + str(InOutPush) + " In out Push Ups")

def lower(level,sender):
    squat = 10 * level
    lunges = 10 * level
    jumpsquat = 10 * level
    bot.send_text_message(sender, "You're new so These Exercises are a good start")
    bot.send_text_message(sender, "Remember no breaks")
    advice = "You should do " + str(squat) + " Squats\n" + str(lunges) + " Lunges"
    bot.send_text_message(sender, advice)
    bot.send_text_message(sender, "And " + str(jumpsquat) + " JumpSquats")

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                        reply_text = getmessage(messaging_text, sender_id)
                        response = reply_text

                    else:
                        messaging_text = 'no text'
                        response = " no text"

                    bot.send_text_message(sender_id, response)

    return "ok", 200


def getmessage(message,senderId):
    message = message.lower()
    if message in GREETINGS or message.find("i have a question") >= 0 or message.find("hey") >= 0 or message.find("hi") >= 0:
        bot.send_text_message(senderId, "Hello! How can I help you?")
        bot.send_text_message(senderId, "Do you want to Lose weight?")
        send_quickreply(senderId, "Do you want to build muscle?")
    elif message.find("bye") >= 0 or message.find("goodbye") >= 0 or message.find("later") >= 0:
        return "Goodbye! Stop by Anytime!"
    elif message in POUNDS:
        if message == "more":
            return "Just keep to the training! You will become fit! ~Sensei Fit!!~"
        else:
            pounds = int(message)
            cals = 3500 * pounds
            base = 10 / 850
            total = base * cals
            per = total / 7
            fin = int(per)
            advice = "Go for a Jog " + str(fin) + " minutes/day for a week"
            bot.send_text_message(senderId, advice)
            bot.send_image_url(senderId, "https://cdn6.aptoide.com/imgs/2/f/9/2f9bd46c3059a2f2506cbc4cd4541ac1_icon.png?w=256")
            return "Do this and You will lose those Pounds!"
    elif message.find("lose weight") >= 0 or message.find("I want to lose weight") >= 0:
        bot.send_text_message(senderId, "Let's burn those Carbs! KA-POW!")
        bot.send_text_message(senderId, "I have A great workout for You!")
        send_quickreplypounds(senderId, "How many pounds would you like to lose?")
    elif message.find("thank") >= 0 or message.find("i can") >= 0 or message == "fine" or message.find("i will do") >= 0 or message.find("great") >= 0 or message.find("okay") >= 0:
        return "So you are doing it! Great you Will see The results"
    elif message.find("hard") >= 0 or message.find("i can't") >= 0 or message.find("cant") >= 0:
        return "You're Strong You can do it!"
    elif message == "no":
        return "Yes! Believe in yourself!"
    elif message == "yes" or message.find("i can") >= 0:
        return "I Believe in You! You have it in you"
    elif message.find("build") >= 0:
        send_quickreplybuild(senderId, "Where of your body do you wanna work out?")
    elif message.find("do i have") >= 0:
        return "You have greatness in you, you can do it"
    elif message in BODY:
        if message == "core":
            core(1, senderId)
        if message == "upper":
            upper(1, senderId)
            bot.send_image_url(senderId, "https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/6c/19/6c/6c196c88-0e97-6341-9120-265189ca6f50/source/256x256bb.jpg")
        if message == "lower":
            lower(1, senderId)
        return "You think you can handle it!?"
    else:
        return "Sorry I don't understand"


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
                    "title": "Lose Weight",
                    "payload": "POSTBACK_PAYLOAD1"
                },
                {
                    "content_type": "text",
                    "title": "Track my progress",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "Build Muscle",
                    "payload": "POSTBACK_PAYLOAD2"
                },
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def send_quickreplypounds(recipient_id, message_text):
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
                    "title": "10",
                    "payload": "POSTBACK_PAYLOAD1"
                },
                {
                    "content_type": "text",
                    "title": "20",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "30",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "40",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "more",
                    "payload": "POSTBACK_PAYLOAD2"
                },
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)

def send_quickreplybuild(recipient_id, message_text):
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
                    "title": "Upper",
                    "payload": "POSTBACK_PAYLOAD1"
                },
                {
                    "content_type": "text",
                    "title": "Lower",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "Core",
                    "payload": "POSTBACK_PAYLOAD2"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True, port=80)
