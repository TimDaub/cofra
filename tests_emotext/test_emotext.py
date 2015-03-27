import re
import sys
import os.path
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

from emotext.apis.text import text_processing
from emotext.apis.text import calc_percentages
from emotext.models.persistence import Emotext
from emotext.models.models import Message
from emotext.models.persistence import MessageCluster
from time import sleep

TEXTS = [
    "Hello. This isn't doge!",
    "Such wow, many pythons!"
]

MESSAGES = [
    Message(entity_name="Testname", text=TEXTS[0]),
    Message(entity_name="OtherTestname", text=TEXTS[1])
]

TOLERANCE_TIME = 1

def test_mc_reset_db():
    """
    Tries to reset the MessageCluster's database.
    """
    mc = MessageCluster()
    mc.reset_db()
    assert len(mc.db.keys()) == 0

def test_mc_add_message():
    """
    Adds multiple messages to the message cluster.
    """
    mc = MessageCluster(TOLERANCE_TIME+3) # 4
    # init message should create a list and start the tolerance counter
    mc.add_message(MESSAGES[0])
    sleep(1)
    # the next message should reset the tolerance counter
    mc.add_message(MESSAGES[1])
    # if it doesn't, conversation should be over after sleep(3)
    sleep(3)
    res = mc.is_conversation_over()
    assert res == False
    sleep(1)
    res = mc.is_conversation_over()
    assert res

def test_mc_counter():
    """
    Initializing a MessageCluster with a custom time.
    """

    mc = MessageCluster(TOLERANCE_TIME)
    mc.start_tolerance()
    sleep(TOLERANCE_TIME+1)

    res = mc.is_conversation_over()
    assert res

def test_text_processing():
    """
    Tests:
        * if strings get separated accordingly
        * words contain punctuation chars
        * if there are sentences that have no words.
        * the number of sentences
    """
    sentences = text_processing(TEXTS[0], stemming=False, remove_punctuation=True)
    assert len(sentences) == 2
    for sentence in sentences:
        assert type(sentence) == type([])
        assert len(sentence) > 0
        for w in sentence:
            # check for punctuation characters in word sequence
            assert re.match(r'[^\w]', w) == None

def test_calc_percentages():
    """
    Tests if a vector of absolute emotion values is calculated correctly by calc_percentages.
    """
    emotions = {
        "love": 27.298217235189718,
        "cry": 17.167578907271867,
        "sadness": 8.795877176280856,
        "boredom": 13.366757881808853,
        "frustration": 7.048259470954596,
        "happiness": 12.981467725924063
    }
    percentages = calc_percentages(emotions)
    sum_values = sum(emotions.values())
    actual_percentages = {k: v/sum_values for k, v in emotions.items() if v != 0}
    for key in emotions.keys():
        assert percentages[key] == actual_percentages[key]


# def test_post_to_entities():
#     """ 
#     Reads all messages of a whatsapp file and posts them as one
#     entity to the server in order to assert them
#     """
    
#     # read messages from a .txt file by using the whatsapp provider
#     messages = get_messages('Tim', r'./providers/static/whatsapp_chat.txt', 'english')
#     for message in messages:
#         r = requests.post(base_url + '/entities/' + message.entity_name, \
#             data=json.dumps(message.__dict__), \
#             headers=headers)
#         res_dict = json.loads(r.text)
#         assert r.status_code <= 200
#         # assert res_dict['entity_name'] == message.entity_name
#         # assert type(res_dict['message']) == type([])
#         # assert len(res_dict['message']) > 0
#         # assert res_dict['date'] == message.date
#         print res_dict