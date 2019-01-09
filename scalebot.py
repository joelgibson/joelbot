import re

ERROR = "Sorry, I didn't understand that"

def no_query_action(context):
    # Interesting stuff here
    return "Hi, what scale would you like to know about?"

# Returns (new_state, new_context, output)
def no_query_on_input(line, context):
    match = re.search(
        pattern=r'What are the notes in ([A-G]) ?(natural|flat|sharp)? ?(major|minor)?',
        string=line,
        flags=re.IGNORECASE)

    if not match:
        return 'NO_QUERY', context, ERROR
    
    key = match.group(1).lower()
    
    return 'PRINT_SCALE', key, None


def print_scale_action(context):
    return f"""Pretend I'm printing {context.upper()} major.
Would you like another?"""

def print_scale_on_input(line, context):
    if 'no' in line.lower():
        return 'END', None, None
    else:
        return 'NO_QUERY', None, None

START_STATE = 'NO_QUERY'

ACTION = {
    'NO_QUERY': no_query_action,
    'PRINT_SCALE': print_scale_action
}
INPUT = {
    'NO_QUERY': no_query_on_input,
    'PRINT_SCALE': print_scale_on_input
}