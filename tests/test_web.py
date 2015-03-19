# py.tests starts tests from /test dir, therefore everything further up
# must first be added to its path
import sys
import os
import requests
import json
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from providers.whatsapp import get_messages
from controllers.config import CfgParser


cfg_p = CfgParser(r'tests/static/test_db.cfg', 'web')

BASE_URL = cfg_p.get_key('HOST')
HEADERS = {
    'Content-type': 'application/json', 
    'Accept': 'text/plain'
}

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
    
def test_get_persons():
    """
    Requests /persons and checks for correctness
    """
    r = requests.get(BASE_URL + '/persons', headers=HEADERS)
    res = json.loads(r.text)
    assert r.status_code <= 200
    assert type(res) == type([])
    if len(res) > 0:
        for person in res:
            assert person['id']
            assert person['timestamp']
            assert person['name']
            traverse(person, assert_persons_attrs)

def assert_persons_attrs(node):
    """
    Asserts a persons attributes using the traverse function.
    """
    assert node['id']
    assert node['key']
    assert node['value'] or node['value'] is None

def traverse(node, fn):
    """
    Traverses a tree structure.
    A asserting function can be passed to check the object
    """
    if len(node['children']) == 0:
        return
    else:
        for child in node['children']:
            fn(child)
            return traverse(child, fn)

if __name__ == '__main__':
    """
    Searches for all functions in this module that 
    have the substring 'test' in them and calls them
    """
    current_module = sys.modules[__name__]
    fnList = [f for f in dir(current_module) if 'test' in f]
    map(lambda s: getattr(current_module, s)(), fnList)