# Import flask with the request object
from flask import Flask, request, jsonify
import requests

import scalebot

# Create the web server
app = Flask(__name__)

# Let's have a nice homepage.
@app.route('/')
def home_page():
    return "Hi, you've reached Joel's server."


# This listens to a slash command from slack. We need to
# remember the current state.
state, context = scalebot.START_STATE, None

@app.route('/scalebot', methods=['POST'])
def scale_bot_endpoint():
    global state, context

    print(request.form)

    line = request.form.get('text')
    state, context, output = scalebot.INPUT[state](line, context)

    if state == 'END':
        state, context = scalebot.START_STATE, None
        return 'Thanks for the chat!'

    output2 = scalebot.ACTION[state](context)

    return f"{output}\n{output2}"


@app.route('/alexa/scalebot')
def alexa_scalebot():
    return ""

# You can message lol_bot via <your website>/lol
#@app.route('/lol')
@app.route('/lol', methods=['POST'])
def lol_bot():
    # Get the value of the 'text' query parameter
    # request.args is a dictionary (cool!)
    #text = request.args.get('text')
    # This bot lols at every command it gets sent!
    #return f'lol {text}'

    # Get the value of the 'text' query parameter
    # request.form is a dictionary (cool!)
    text = request.form.get('text')
    modified = "".join(c+c for c in text)
    return f'lol {modified}'

def send_message(channel, text):
    headers = {
        'Authorization': 'Bearer ' + 'a1RVVG8u7Rp2ByCIDjFRYu0D-927726508815-772081506015-bxox'[::-1],
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'channel': channel
    }
    return requests.post(
        'https://slack.com/api/chat.postMessage',
        json=data,
        headers=headers)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    content = request.get_json()

    if content['type'] == 'url_verification':
        return jsonify({'challenge': content['challenge']})
    
    if content['type'] == 'event_callback':
        event = content['event']
        if event.get('subtype', None) != 'bot_message':
            send_message(
                channel=event['channel'],
                text=f"You said: {event['text']}")
            return "Ok done, have a nice day"
    
    print(content)
    return "Didn't do anything"




@app.route('/alexa', methods=['POST', 'GET'])
def alexa():
  return jsonify({
    'version': '0.1',
    'response': {
        "outputSpeech": {
            "type": "SSML",
            #"text": "Plain text string to speak",
            "ssml": '<speak><prosody pitch="+0%">hello</prosody> <prosody pitch="+30%">hello</prosody> <prosody pitch="-30%">hello</prosody></speak>',
            "playBehavior": "REPLACE_ENQUEUED"      
        },
    }
  })



# Start the web server!
if __name__ == '__main__':
    app.run()