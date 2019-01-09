import re
import random

ERROR_MESSAGE = "Sorry, I didn't understand that"
TUTORS = ['Nicky', 'Tim', 'Seb', 'Owen']

# List of states used in the program. 'START' and 'END'
# are special, and used by the frontends.
STATES = ['START', 'ASK_WHERE', 'SEND_HELP', 'END']

# Each action takes in the current context, and returns
# a string (or in the future, some more complicated thing)
# to be displayed to the user.
def start_action(context):
    return "How can I help?"

# Each input function is given both the line of input and
# the current context, and returns a triple of
# 0. The new state to transition to
# 1. The updated context
# 2. A string to display (usually for error handling), or None.
def start_input(line, context):
    # "Help, I'm locked out of Langley"
    # "I'm locked out in Main"
    match = re.search(r'locked out.*(of|in) (.+)', line, re.IGNORECASE)
    if match:
        place = match.group(2).title()
        return ('SEND_HELP', {'location': place}, None)
    
    # "Help, I'm locked out!"
    # "Help!"
    match = re.search(r'help|locked out', line, re.IGNORECASE)
    if match:
        return ('ASK_WHERE', {}, None)
    
    # Didn't understand.
    return ('START', {}, ERROR_MESSAGE)

def ask_where_action(context):
    return "Where are you?"

def ask_where_input(line, context):
    # "I'm in Main"
    match = re.search(r'in (.+)', line, re.IGNORECASE)
    if match:
        place = match.group(1).title()
        return ('SEND_HELP', {'location': place}, None)
    
    # Didn't understand.
    return ('ASK_WHERE', {}, ERROR_MESSAGE)


def send_help_action(context):
    # Randomly choose a tutor, and I guess do something
    # "In the real world" to dispatch them.
    tutor = random.choice(TUTORS)
    place = context['location']

    return f"I've sent {tutor} to {place}. Do you need more help?"

def send_help_input(line, context):
    # If they don't need more help, go to the special 'END' state.
    
    if 'no' in line.lower():
        return ('END', {}, "Enjoy your evening")
    else:
        return ('START', {}, None)


ACTION = {
    'START': start_action,
    'ASK_WHERE': ask_where_action,
    'SEND_HELP': send_help_action
}
INPUT = {
    'START': start_input,
    'ASK_WHERE': ask_where_input,
    'SEND_HELP': send_help_input
}