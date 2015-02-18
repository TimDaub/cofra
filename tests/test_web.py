import requests
import sys

base_url = 'http://localhost:5000'
entity_name = 'testname'

def test_post_to_entities():
    """ Sends a post request to /entities and asserts its status """
    r = requests.post(base_url + '/entities/' + entity_name)
    assert r.status_code <= 200
    assert r.text == entity_name


if __name__ == '__main__':
    """ Searches for all functions in this module that have the substring 'test' in them and calls them """
    current_module = sys.modules[__name__]
    fnList = [f for f in dir(current_module) if 'test' in f]
    map(lambda s: getattr(current_module, s)(), fnList)