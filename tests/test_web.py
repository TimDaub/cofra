import requests
import sys
import os.path
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from providers.whatsapp import get_messages

base_url = 'http://localhost:5000'
headers = {
    'Content-type': 'application/json', 
    'Accept': 'text/plain'
}

def test_post_to_entities():
    """ 
    Reads all messages of a whatsapp file and posts them as one
    entity to the server in order to assert them
    """
    
    # read messages from a .txt file by using the whatsapp provider
    messages = get_messages('Tim', r'./providers/static/whatsapp_chat.txt', 'english')
    for message in messages:
        r = requests.post(base_url + '/entities/' + message.entity_name, \
            data=json.dumps(message.__dict__), \
            headers=headers)
        # res_dict = json.loads(r.text)
        assert r.status_code <= 200
        # assert res_dict['entity_name'] == message.entity_name
        # assert type(res_dict['message']) == type([])
        # assert len(res_dict['message']) > 0
        # assert res_dict['date'] == message.date
        # print res_dict
    


if __name__ == '__main__':
    """
    Searches for all functions in this module that 
    have the substring 'test' in them and calls them
    """
    current_module = sys.modules[__name__]
    fnList = [f for f in dir(current_module) if 'test' in f]
    map(lambda s: getattr(current_module, s)(), fnList)