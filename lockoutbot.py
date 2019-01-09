import re
import random

# List of states used in the program. 'START' and 'END'
# are special, and used by the frontends.
STATES = ['START', 'ASK_WHERE', 'SEND_HELP', 'END']


ERROR_MESSAGE = "Sorry, I didn't understand that"
TUTORS = ['Nicky', 'Tim', 'Seb', 'Owen']

def start_action(context):
    return "How can I help?"

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
    
    return ('START', {}, ERROR_MESSAGE)

def ask_where_action(context):
    return "Where are you?"

def ask_where_input(line, context):
    # "I'm in Main"
    match = re.search(r'in (.+)', line, re.IGNORECASE)
    if match:
        place = match.group(1).title()
        return ('SEND_HELP', {'location': place}, None)
    
    return ('ASK_WHERE', {}, ERROR_MESSAGE)


def send_help_action(context):
    # Randomly choose a tutor, and I guess do something
    # "In the real world" to dispatch them.
    tutor = random.choice(TUTORS)
    place = context['location']

    return f"I've sent {tutor} to {place}. Do you need more help?"

def send_help_input(line, context):
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