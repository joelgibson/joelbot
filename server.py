# Import flask with the request object
from flask import Flask, request

# Create the web server
app = Flask(__name__)

# Let's have a nice homepage.
@app.route('/')
def home_page():
    return "Hi, you've reached Joel's server."


# Listen to /lockout from slack. The state and context are global.
import lockoutbot
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
    output2 = scalebot.ACTION[state](context)

    # Smoosh the outputs together, taking into account the fact that
    # the first output might be None.
    if output1:
        return f"{output1}\n{output2}"

    return output2


# Start the web server!
if __name__ == '__main__':
    app.run()