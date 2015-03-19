import re
from utils.utils import conv_to
from models.models import Message
from datetime import datetime

def get_messages(entity_name, filepath='providers/static/whatsapp_chat.txt', language='english'):
    """ 
    Reads the messaging history from a .txt file and extracts and filters
    it for a certain entity.
    """
    message_pattern = """
    ^                           # begin of line
    (\d{2}).(\d{2}).(\d{2})     # match date DD.MM.YY
    \s
    (\d{2}):(\d{2}):(\d{2}):    # match time HH.MM.SS
    \s
    (.*):                       # match entity's user name
    \s
    (.*)                        # match entity's message
    $                           # end of line
    """
    # uses message_pattern to extract time, date, entity name and message from a line-string
    # then uses map function to convert datatypes of tuple into ints if possible, otherwise leave them as
    # strings
    parsed_messages = [map(conv_to(int), re.search(message_pattern, l, re.VERBOSE).groups()) \
                         for l in (open(filepath, 'r')) \
                         if re.match(r'^\n$', l) == None]
    # convert tuples into Message objects and add 2000 years to year as whatsapp notates it YY and not YYYY
    # also filters for an entity name
    messages_list = [Message(m[6], m[7], datetime(m[2]+2000, m[1], m[0], m[3], m[4], m[5]).strftime('%Y-%m-%dT%H:%M:%S'), language) \
                        for m in parsed_messages \
                        if m[6] == entity_name]
    return messages_list