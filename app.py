import os, sys
from flask import Flask, request
from pymessenger import Bot
import requests
import json
import random
from Credentials import *
import sqlite3

app = Flask(__name__)


bot = Bot(PAGE_ACCESS_TOKEN)
GREETINGS = ['is anyone available to chat?', 'wah gwaan', 'sup','hey','hi','yo','hello','good afternoon', 'howdy', 'i have a question']
    
def populate_table():
    try: 
        conn = sqlite3.connect('work.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS work (
                    name text,
                    category text,
                    imageurl text,
                    videourl text
                    )""")
        c.execute("SELECT * FROM work")
        if c.fetchone() == None or c.fetchone() == 0:    
            c.execute("INSERT INTO work VALUES ('push ups','upper','https://is1-ssl.mzstatic.com/image/thumb/Purple49/v4/35/5a/20/355a2080-406c-e1a5-9f12-b91bf13de0d0/source/256x256bb.jpg','https://www.youtube.com/watch?v=ZWdBqFLNljc')")
            c.execute("INSERT INTO work VALUES ('crunches','core','https://www.flashmavi.com/med_old/src/weight_training_abs_crunches.png','https://www.youtube.com/watch?v=_M2Etme-tfE')")
            c.execute("INSERT INTO work VALUES ('air bike','core','https://is2-ssl.mzstatic.com/image/thumb/Purple124/v4/ca/12/14/ca1214ad-0785-1a60-1c38-e34db666bb2d/source/256x256bb.jpg','https://www.youtube.com/watch?v=jKT7-9L935g')")
            c.execute("INSERT INTO work VALUES ('inout push up','upper','https://is1-ssl.mzstatic.com/image/thumb/Purple113/v4/9a/23/33/9a233351-d24f-4fe3-1828-ccccf26c7c0a/source/256x256bb.jpg','https://www.youtube.com/watch?v=S7665-gzbTc')")
            c.execute("INSERT INTO work VALUES ('diamond push up','upper','https://is1-ssl.mzstatic.com/image/thumb/Purple113/v4/9a/23/33/9a233351-d24f-4fe3-1828-ccccf26c7c0a/source/256x256bb.jpg','https://www.youtube.com/watch?v=jaxbEHLC4qU')")
            c.execute("INSERT INTO work VALUES ('reverse crunches','core','https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/8c/3d/85/8c3d858a-90db-dd05-463c-a7d8e52a8d86/source/256x256bb.jpg','https://www.youtube.com/watch?v=OzRiZ6QgnTA')")
            c.execute("INSERT INTO work VALUES ('kneeling plank','core','https://is4-ssl.mzstatic.com/image/thumb/Purple123/v4/27/fd/2d/27fd2df2-d17b-b79a-b767-0ffd785a2854/source/256x256bb.jpg','https://www.youtube.com/watch?v=Ns1NS9ThNhI')")
            c.execute("INSERT INTO work VALUES ('plank','core','https://is4-ssl.mzstatic.com/image/thumb/Purple123/v4/27/fd/2d/27fd2df2-d17b-b79a-b767-0ffd785a2854/source/256x256bb.jpg','https://www.youtube.com/watch?v=TvxNkmjdhMM')")
            c.execute("INSERT INTO work VALUES ('mountain climber','core','https://rejuvage.com/wp-content/uploads/2019/07/iStock-957699448.jpg','https://www.youtube.com/watch?v=nmwgirgXLYM')")
            c.execute("INSERT INTO work VALUES ('squat','lower','https://is3-ssl.mzstatic.com/image/thumb/Purple118/v4/57/87/0e/57870e6d-1f62-0019-62a4-7cade5b5d16e/source/256x256bb.jpg','https://www.stack.com/a/squat-how-to')")
            c.execute("INSERT INTO work VALUES ('lunges','lower','https://us.123rf.com/450wm/artinspiring/artinspiring1903/artinspiring190300466/124593050-stock-vector-woman-making-lunges-doing-sport-exercises-in-gym-leg-workout-muscle-building-healthy-and-active-life.jpg?ver=6','https://www.youtube.com/watch?v=7SMzPn4LGjQ')")
            c.execute("INSERT INTO work VALUES ('lung knee up','lower','https://i.pinimg.com/originals/eb/28/33/eb283322b48ec6809eb28e085c3fd465.jpg','https://www.youtube.com/watch?v=KEtmkmTq0Ec')")
            c.execute("INSERT INTO work VALUES ('jump Squat','lower','https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/1207-lean-toned-1-1441032989.jpg','https://www.youtube.com/watch?v=We1xYHGTxQw')")
            c.execute("INSERT INTO work VALUES ('wide squat','lower','https://i.pinimg.com/originals/a0/1f/13/a01f136adebd96e0a78fb49aafeee4d5.png','https://www.youtube.com/watch?v=v2ukjHXbXVo')")
            c.execute("INSERT INTO work VALUES ('russian twist','core','https://image.shutterstock.com/image-vector/woman-doing-russian-twist-exercise-260nw-1316827436.jpg','https://www.youtube.com/watch?v=NeAtimSCxsY')")
            c.execute("INSERT INTO work VALUES ('pull ups','upper','https://cdn-xi3mbccdkztvoept8hl.netdna-ssl.com/wp-content/uploads/watermarked/Pullup_M_WorkoutLabs.png','https://www.youtube.com/watch?v=iUNoLR0pYjY')")
            conn.commit()
            c.close()
            conn.close()
    except sqlite3.Error as e:
        print(e)
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                    psid TEXT,
                    start_weight INTEGER,
                    current_date ,
                    videourl text
                    )""")

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200

mainTag = 0
currPath = 1
workoutTag = None
currWorkPath = 0

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    global mainTag
    global currPath
    global workoutTag
    bot_id = data["entry"][0]["id"]
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                senderId = messaging_event['sender']['id']
                if(senderId != bot_id):
                    recipient_id = messaging_event['recipient']['id']
                
                    if messaging_event.get('message'):
                        if 'text' in messaging_event['message']:
                            messaging_text = messaging_event['message']['text'].lower()
                            if messaging_text in GREETINGS:
                                mainTag = 1
                                currPath = 1
                                workoutTag = None
                                handleMessage(messaging_text, senderId)
                            elif messaging_text == "lose weight" or mainTag == 2:
                                mainTag = 2
                                handleMessage(messaging_text, senderId)
                            elif messaging_text == "give me a workout" or mainTag == 3:
                                mainTag = 3
                                handleMessage(messaging_text, senderId)
                            elif messaging_text == "find an exercise" or mainTag == 4:
                                mainTag = 4
                                handleMessage(messaging_text, senderId)
                            else:
                                mainTag = 5
                                handleMessage(messaging_text, senderId)
                                
                        else:
                            messaging_text = 'no text'
                            response = " no text"

                        

    return "ok", 200


def handleMessage(message,senderId):
    # message = message.lower()
    global mainTag
    global currPath
    global workoutTag
    if mainTag == 1: 
        userfname = json.loads(getFirstName(senderId))
        bot.send_text_message(senderId, "Hi " +userfname.get("first_name")+ ", Welcome to Fit Sensei.")
    #    bot.send_text_message(senderId, "Do you want to Lose weight?")      
        send_quickreplyinit(senderId, "What would you like to do?")
    elif mainTag == 2:
        if currPath == 1:
             bot.send_text_message(senderId, "So you would like to lose weight, You've come to the right place")
             bot.send_text_message(senderId, "How many pounds do you currently weigh?")
             currPath = 2
        elif currPath == 2:
            if message.isnumeric():
                response = "Okay! and how many pounds would you like to lose?"
                bot.send_text_message(senderId, response)
                currPath = 3
            else:
                response = "Sorry but that is not a valid weight"
                bot.send_text_message(senderId, response)
                bot.send_text_message(senderId, "How many pounds do you currently weigh?")
                currPath = 2
        elif currPath == 3:
            if message.isnumeric():
                response = "Great! How tall are you (in cm)?"
                bot.send_text_message(senderId, response)
                currPath = 4
            else:
                response = "Sorry but that is not a valid amount of pounds..."
                bot.send_text_message(senderId, response)
                bot.send_text_message(senderId, "How many pounds would you like to lose")
                currPath = 3
        elif currPath == 4:
            if message.isnumeric():
                bot.send_text_message(senderId, "Noted... How many days do you work out in a week?")            
                currPath = 5
            else:
                response = "Sorry but that is not a valid height..."
                bot.send_text_message(senderId, response)
                bot.send_text_message(senderId, "How tall are you? (in cm)")
                currPath = 4
        elif currPath == 5:
            if message.isnumeric() and (int(message) >= 0 and int(message) <=7):
                bot.send_text_message(senderId, "Creating Workout... ")     
                sendAction(senderId)
                currPath = 6
            else:
                response = "Sorry but that is not a valid number of days"
                bot.send_text_message(senderId, response)
                bot.send_text_message(senderId, "How many days do you work out in a week?")
                currPath = 5
    elif mainTag == 3:
        if currPath == 1:
            response = "So you want the Fit Sensei to give you a workout huh? I'll give you the workout of your life"
            bot.send_text_message(senderId, response)
            send_quickreplyWorkout(senderId, "Where do you want to focus on?")
            currPath = 2
        elif currPath == 2:
            if message == "lower body" or message == "lower" or workoutTag == "lower":
                workoutTag = "lower"
            elif message == "core" or workoutTag == "core":
                workoutTag = "core"
            elif message == "upper body" or message == "upper" or workoutTag == "upper":
                workoutTag = "upper"
            send_quickreplydiff(senderId, "How intense do you want the workout?")
            currPath = 3
        elif currPath == 3:
            if message == "easy" or message == "medium" or message == "hard":
                bot.send_text_message(senderId, "Here is a workout for you!")
                generateWorkout(senderId, workoutTag, message)                    
        else:
            pass
    elif mainTag == 4: 
        if currPath == 1:
            bot.send_text_message(senderId, "You wish to learn about an exersise I see")
            bot.send_text_message(senderId, "Well you've come to the right sensei")
            bot.send_text_message(senderId, "What exercise would you like to know about?")
            currPath = 2
        elif currPath == 2:
            findExercise(senderId, message)
    else:
        response = "I don't understand you"
        bot.send_text_message(senderId, response)   
    #elif message.find("bye") >= 0 or message.find("goodbye") >= 0 or message.find("later") >= 0:
     #   return "Goodbye! Stop by Anytime!"
   # elif message in POUNDS:
    #    if message == "more":
   #         return "Just keep to the training! You will become fit! ~Sensei Fit!!~"
  #      else:
  #          pounds = int(message)
   #         cals = 3500 * pounds
    #        base = 10 / 850
    #        total = base * cals
     #       per = total / 7
     #       fin = int(per)
    #        advice = "Go for a Jog " + str(fin) + " minutes/day for a week"
    #        bot.send_text_message(senderId, advice)
    #        bot.send_image_url(senderId, "https://cdn6.aptoide.com/imgs/2/f/9/2f9bd46c3059a2f2506cbc4cd4541ac1_icon.png?w=256")
    #        return "Do this and You will lose those Pounds!"
   # elif message.find("lose weight") >= 0 or message.find("I want to lose weight") >= 0:
    #    bot.send_text_message(senderId, "Let's burn those Carbs! KA-POW!")
    #    bot.send_text_message(senderId, "I have A great workout for You!")
      #  send_quickreplypounds(senderId, "How many pounds would you like to lose?")
    #elif message.find("thank") >= 0 or message.find("i can") >= 0 or message == "fine" or message.find("i will do") >= 0 or message.find("great") >= 0 or message.find("okay") >= 0:
    #    return "So you are doing it! Great you Will see The results"
    #elif message.find("hard") >= 0 or message.find("i can't") >= 0 or message.find("cant") >= 0:
   #     return "You're Strong You can do it!"
   # elif message == "no":
  #      return "Yes! Believe in yourself!"
   # elif message == "yes" or message.find("i can") >= 0:
   #     return "I Believe in You! You have it in you"
   # elif message.find("build") >= 0:
   #     send_quickreplybuild(senderId, "Where of your body do you wanna work out?")
   # elif message.find("do i have") >= 0:
    #    return "You have greatness in you, you can do it"
   # elif message in BODY:
  #      if message == "core":
  #          core(1, senderId)
  #      if message == "upper":
    #        upper(1, senderId)
    #        bot.send_image_url(senderId, "https://is2-ssl.mzstatic.com/image/thumb/Purple118/v4/6c/19/6c/6c196c88-0e97-6341-9120-265189ca6f50/source/256x256bb.jpg")
    #    if message == "lower":
    #        lower(1, senderId)
    #    return "You think you can handle it!?"
    #else:
     #   return "Sorry I don't understand"
def generatePlan(senderId)
    

def generateWorkout(senderId, category, difficulty):
    random.seed()
    populate_table()
    if difficulty == "easy":
        reps = random.randint(10, 15)
    elif difficulty == "medium":
        reps = random.randint(10, 15) * 2
    else:
        reps = random.randint(10, 15) * 3
    conn = sqlite3.connect('work.db')

    b = conn.cursor()

    b.execute("SELECT * FROM work WHERE category =? ", (category,))
    hold = b.fetchall()
    for ex in hold:
        bot.send_text_message(senderId, "You must do " +str(reps)+ " " +ex[0])
    bot.send_text_message(senderId, "I believe in you")
    conn.commit()
    b.close()
    conn.close()

def findExercise(senderId, message):
    conn = sqlite3.connect('work.db')

    b = conn.cursor()
    elements = []
    b.execute("SELECT * FROM work WHERE name =? ", (message,))
    ex = b.fetchone()
    if ex == None or ex == "None":
        bot.send_text_message(senderId, "I don't know about that exercise but I'm sure I will soon")
    else:
        element = {
            'title': ex[0],
            'buttons': [{
                'type': 'web_url',
                'title': 'Check Out',
                'url': ex[3]
            }],
            'image_url': ex[2]
        }
        elements.append(element)
        bot.send_text_message(senderId, "Here you go!")
        sendAction(senderId)
        bot.send_generic_message(senderId, elements)
    conn.commit()
    b.close()
    conn.close()
 
def sendAction(recepientId):
    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('access_token', PAGE_ACCESS_TOKEN),
    )

    data = json.dumps({"recipient": {"id": recepientId}, "sender_action": "typing_on"})

    response = requests.post('https://graph.facebook.com/v2.6/me/messages', headers=headers, params=params, data=data) 

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
                    "title": "Reach my goals",
                    "payload": "POSTBACK_PAYLOAD1"
                },
                {
                    "content_type": "text",
                    "title": "Find an exercise",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "Track my progress",
                    "payload": "POSTBACK_PAYLOAD3"
                },
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)



def send_quickreplyinit(recipient_id, message_text):
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
                    "title": "Lose weight",
                    "payload": "POSTBACK_PAYLOAD1"
                },
                {
                    "content_type": "text",
                    "title": "Give me a workout",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "Find an exercise",
                    "payload": "POSTBACK_PAYLOAD3"
                },
                                {
                    "content_type": "text",
                    "title": "Track my progress",
                    "payload": "POSTBACK_PAYLOAD3"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)

def send_quickreplyWorkout(recipient_id, message_text):
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
                    "title": "Upper Body",
                    "payload": "POSTBACK_PAYLOAD1"
                },
                {
                    "content_type": "text",
                    "title": "Core",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "Lower Body",
                    "payload": "POSTBACK_PAYLOAD3"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v7.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)
    
def send_quickreplydiff(recipient_id, message_text):
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
                    "title": "Easy",
                    "payload": "POSTBACK_PAYLOAD1"
                },
                {
                    "content_type": "text",
                    "title": "Medium",
                    "payload": "POSTBACK_PAYLOAD2"
                },
                {
                    "content_type": "text",
                    "title": "Hard",
                    "payload": "POSTBACK_PAYLOAD3"
                }
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

def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True, port=80)
