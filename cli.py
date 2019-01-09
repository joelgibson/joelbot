import scalebot

state, context = scalebot.START_STATE, None

while state != 'END':
    output = scalebot.ACTION[state](context)
    print(output)

    line = input("Prompt> ")
    state, context, output = scalebot.INPUT[state](line, context)

    if output != None:
        print(output)