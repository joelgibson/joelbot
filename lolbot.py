# Import flask with the request object
from flask import Flask, request

# Create the web server
app = Flask(__name__)

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

@app.route('/alexa', methods=['POST', 'GET'])
def alexa():
  return jsonify({
    'version': '0.1',
    'response': {
        "outputSpeech": {
            "type": "SSML",
            #"text": "Plain text string to speak",
            "ssml": '<prosody pitch="+0%">hello</prosody> <prosody pitch="+30%">hello</prosody> <prosody pitch="-30%">hello</prosody>',
            "playBehavior": "REPLACE_ENQUEUED"      
        },
    }
  })



# Start the web server!
if __name__ == '__main__':
    app.run()