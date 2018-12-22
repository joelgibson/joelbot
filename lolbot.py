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
    modified = str.join(c+c for c in text)
    return f'lol {modified}'



# Start the web server!
if __name__ == '__main__':
    app.run()