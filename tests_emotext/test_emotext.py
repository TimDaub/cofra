import re
import sys
import os.path


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from controllers.config import CfgParser
from models.et_middleware import Emotext


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')
from emotext.apis.text import text_processing
from emotext.apis.text import calc_percentages
from emotext.models.models import CacheController
from emotext.models.models import Conversation

cfg_et_graph = CfgParser(r'../emotext/config.cfg', 'graph_search')
cfg_et_cn = CfgParser(r'../emotext/config.cfg', 'conceptnet5_parameters')
MAX_DEPTH = cfg_et_graph.get_key('MAX_DEPTH', method_name='getint')
MIN_WEIGHT = cfg_et_graph.get_key('MIN_WEIGHT', method_name='getint')
REQ_LIMIT = cfg_et_cn.get_key('REQ_LIMIT', method_name='getint')

TEXTS = [
    "Hello. This isn't doge!",
    "Such wow, many pythons!"
]

def test_interpolating_emotions_vector():
    """
    From CacheController we take a bunch of emotion-vectors and submit them to a conversation's 
    interpolation method, to test it.
    """
    cc = CacheController(max_depth=MAX_DEPTH, min_weight=MIN_WEIGHT, req_limit=REQ_LIMIT)
    c = Conversation([])
    c.word_interpolation(cc.cache)

def test_init_cachectrl():
    """
    Tries to initialize a CacheController object and checks his instance type.
    """
    cc = CacheController(max_depth=MAX_DEPTH, min_weight=MIN_WEIGHT, req_limit=REQ_LIMIT)
    assert isinstance(cc, CacheController)

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

# deprecate this function?
# 
# 
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