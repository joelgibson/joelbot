# Lockout Bot

A worked example of a lockout bot, for the #botstream. Read the files (and the comments in the code) in this order:

1. Check out the [conversation diagram](conversation_diagram.jpg).
2. Check out the [lockoutbot.py](lockoutbot.py), it is a direct translation from the diagram.
3. Check out the [cli.py](cli.py) for the command-line interface.
4. Check out the [server.py](server.py) for the flask endpoints. The first endpoint is a slash command in Slack, and the second endpoint is an Alexa bot.