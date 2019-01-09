from flask import Flask, request, jsonify
import lockoutbot

app = Flask(__name__)

# Let's have a nice homepage.
@app.route('/')
def home_page():
    return "Hi, you've reached Joel's server."


# Listen to /lockout from slack. The state and context are global, so
# there is only a single conversation running with lockout bot at a time.
state, context = 'START', {}

@app.route('/lockoutbot', methods=['POST'])
def lockoutbot_endpoint():
    global state, context

    # The user has just given us a line of input. Request the next
    # state transition, context, and optional output. We save the
    # output for later, since we still have to perform the action for
    # the new state.
    line = request.form.get('text')
    state, context, output1 = lockoutbot.INPUT[state](line, context)

    # The special 'END' state here should reset the bot, so that the
    # next slash command is back at the start.
    if state == 'END':
        state, context = 'START', {}
        return 'Thanks for the chat!'

    # Perform the action for the new state
    output2 = lockoutbot.ACTION[state](context)

    # Smoosh the outputs together, taking into account the fact that
    # the first output might be None.
    if output1:
        return f"{output1}\n{output2}"

    return output2

@app.route('/alexa/lockoutbot', methods=['GET', 'POST'])
def lockoutbot_alexa_endpoint():
    global state, context
    print(request.get_json())

    request_data = request.get_json()
    request_type = request_data['request']['type']
    try:
        request_query = request_data['request']['intent']['slots']['query']['value']
    except KeyError:
        request_query = ''

    request_type = request.json['request']['type']
    output = ''

    # We are starting, so we should reset the state
    if request_type == 'LaunchRequest':
        state, context = 'START', {}
        print('Launched, resetting state')
    elif request_type == 'IntentRequest':
        print(f'Processing {request_query} with ({state}, {context})')
        # Intents will have some input, so we need to process it
        # Change the conversation state based on the message from the user
        state, context, output1 = lockoutbot.INPUT[state](request_query, context)
        if output1:
            output += output1 + '\n'
        print(f'Result ({state}, {context})')

    # Do something based on the state
    print(f'Starting action ({state}, {context})')
    output += lockoutbot.ACTION[state](context)

    print(f'Giving response {output}')

    return jsonify({
        'version': '0.1',
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': f"""<speak><voice name="Joey">{output}</voice></speak>"""
            }
        }
    })


if __name__ == '__main__':
    app.run()