from flask import Flask, request
import os
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from googletrans import Translator

from commands.url_shortner import url_shortner
from commands.random_joke import random_joke
from commands.random_quote import random_quote
from commands.fibonacci import fibonacci_generator
from commands.youtube_search import youtube_search
from commands.qrcode_generator import text_to_qrcode
from fetchData import fetch_questions
from postQuestion import post_user_question

app = Flask(__name__)

BOT_ID = os.environ.get('BOT_ID')

questions_dict = fetch_questions(BOT_ID)

@app.route("/")
def hello():
    return "Status Online"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False


    if incoming_msg in questions_dict:
        text = questions_dict[incoming_msg]
        msg.body(text)
        responded = True
    else:

        if 'question:' in incoming_msg and 'answer:' in incoming_msg and 'password:' in incoming_msg and responded == False:
            question_index = incoming_msg.index(':')
            answer_index = incoming_msg.index('answer:')
            password_index = incoming_msg.index('password:')

            question = incoming_msg[question_index + 1:answer_index].strip()
            answer = incoming_msg[answer_index + 7:password_index].strip()
            password = incoming_msg[password_index + 9:].strip()

            if password == str(BOT_ID):
                post_user_question(question, answer)
                text = 'Question added.'
            else:
                text = 'Invalid password.'
            
            msg.body(text)
            responded = True

        if 'start' == incoming_msg and responded == False:
            text = f'🤖 Hello!\ni am Bot created by Azzam, how can i help you?\n'\
            '\nCommands are:\n'\
            '\nShorten Url by : url <your link>'\
            '\nYoutube searching by : youtube <your keyword>'\
            '\nRandom Joke by : joke'\
            '\nRandom Quote by : quote'\
            '\nRandom Cat by : cat'\
            '\nGet Fibonacci for my number : fibonacci <your number>'\
            '\nHelp view commands by : help'
            msg.body(text)
            responded = True

        if 'url' == incoming_msg.split(' ')[0] and responded == False:
            text = "Error"
            url = incoming_msg.split(' ')[1]
            try:
                new_url = url_shortner(url)
                text = new_url
            except Exception:
                text = "Sorry, invalid url."
            finally:
                msg.body("URL: " + text)
                responded = True

        if 'joke' == incoming_msg and responded == False:
            msg.body("Joke: " + random_joke())
            responded = True

        if 'quote' == incoming_msg:
            msg.body("Quote: " + random_quote())
            responded = True

        if 'fibonacci' == incoming_msg.split(' ')[0] and responded == False:
            text = "Error"
            try:
                user_int = int(incoming_msg.replace("fibonacci", "").strip())
                text = f"{user_int} Fibonacci number are : {fibonacci_generator(user_int)}"
            except  Exception:
                pass
            msg.body(text)
            responded = True

        if 'youtube' == incoming_msg.split(' ')[0] and responded == False:
            text = "Error"
            try:
                user_input = incoming_msg[7:]
                result = youtube_search(user_input)
                text = ""
                for i in result:
                    text += i + "\n\n"
            except Exception:
                pass
            msg.body(text)
            responded = True

        if 'cat' == incoming_msg and responded == False:
            msg.media('https://cataas.com/cat')
            responded = True

        # if 'qrcode' in incoming_msg:
        #     try:
        #         user_input = incoming_msg[7:]
        #         msg.media(text_to_qrcode(user_input))
        #     except Exception:
        #         msg.body("Error")
        #     responded = True

        if 'help' == incoming_msg and responded == False:
            text = f'Commands are:\n'\
                '\nShorten url by : url <your link>'\
                '\nYoutube searching by : youtube <your keyword>'\
                '\nRandom Joke by : joke'\
                '\nRandom Quote by : quote'\
                '\nRandom Cat by : cat'\
                '\nGet Fibonacci for my number : fibonacci <your number>'
            msg.body(text)
            responded = True

    if responded == False:
        msg.body('Sorry! the bot does not support your command, type "help" to view supported commands.')

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=4000, debug=True)
