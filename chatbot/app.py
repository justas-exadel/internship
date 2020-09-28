import datetime
from flask import Flask, request
from pymessenger.bot import Bot
from keys import ACCESS_TOKEN, VERIFY_TOKEN

app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

class Meanings:
    time_meanings = ['what time is it', 'what time is it?', 'what time is?',
                     'what time is']


@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    inputs = message['message'].get('text')
                    if inputs.lower() in Meanings.time_meanings:
                        ts = output["entry"][0]["messaging"][0]["timestamp"]
                        response_sent_text = time_now(ts)                        
                        send_message(recipient_id, response_sent_text)
                    else:
                        response_sent_text = 'Did not understand the question.'
                        send_message(recipient_id, response_sent_text)
    return "Message Processed"


def time_now(timestamp):
    dts = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    now = dts.strftime("%H:%M")    
    return str(now)


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:       
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def send_message(recipient_id, response):   
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()
