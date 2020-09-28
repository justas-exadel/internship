<<<<<<< HEAD
import datetime
=======
import time
>>>>>>> 3133489525a58287346d60c29684b30c3f789881
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
<<<<<<< HEAD
ACCESS_TOKEN = 'EAAN2FELYrhoBADSxFlpPc7NlqjZCjpKwZCoOlSme7xU7rsE6MMGfGIBvQPZCbprtDNWWUl8ZCrZCF1vchBdfL4PUrKayz56eGR7IT0OefxreqLkRtO6bw8zfB9ola2WlKfWhYisl5MWZBZBSjmjCHhZAfXZBTNZAu2yZCZBS9gjUo9RHMwZDZD'
=======
ACCESS_TOKEN = 'EAAN2FELYrhoBAErHqGR7wpNY9UgabZAP8U1TejpoJZApRsEVxe6EjfaYQdHXxflakHVBOFds7C6Gu0zkDtIJfml5mUvm2OTZBDF2ksMBZC2W4RsfkXkgyuDOqWEHNZBkD52kRorq7vcTMu1PCsfK31ZBOmyxLdQdmAJcUZCD0ip9QZDZD'
>>>>>>> 3133489525a58287346d60c29684b30c3f789881
VERIFY_TOKEN = 'secret'
bot = Bot(ACCESS_TOKEN)

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
                    if inputs.lower() in time_meanings:
<<<<<<< HEAD
                        ts = output["entry"][0]["messaging"][0]["timestamp"]
                        response_sent_text = time_now(ts)
=======
                        response_sent_text = time_now()
>>>>>>> 3133489525a58287346d60c29684b30c3f789881
                        send_message(recipient_id, response_sent_text)
                    else:
                        response_sent_text = 'Did not understand the question.'
                        send_message(recipient_id, response_sent_text)
    return "Message Processed"


<<<<<<< HEAD
def time_now(timestamp):
    dts = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    now = dts.strftime("%H:%M")
=======
def time_now():
    now = time.strftime("%H:%M")
>>>>>>> 3133489525a58287346d60c29684b30c3f789881
    return str(now)


def verify_fb_token(token_sent):
<<<<<<< HEAD
    if token_sent == VERIFY_TOKEN:
=======
    if token_sent == VERIFY_TOKEN:       
>>>>>>> 3133489525a58287346d60c29684b30c3f789881
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


<<<<<<< HEAD
def send_message(recipient_id, response):
    print(request.data)
=======
def send_message(recipient_id, response):   
>>>>>>> 3133489525a58287346d60c29684b30c3f789881
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()
