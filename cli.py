import lockoutbot
bot = lockoutbot

# Perform the action going into the initial state.
state, context = 'START', {}
output = bot.ACTION[state](context)
print(output)

while True:
    # Read a line of input from the user, and request the next state
    # transition, context, and optional output.
    line = input("Prompt> ")
    state, context, output = bot.INPUT[state](line, context)

    # The special 'END' state terminates the cli.
    if state == 'END':
        break

    # The output returned from the state transition might be None.
    if output != None:
        print(output)
    
    # Perform the next bot action, and show any output to the user.
    output = bot.ACTION[state](context)
    print(output)