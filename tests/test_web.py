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
from models.models import Person

cfg_p = CfgParser(r'tests/static/test_db.cfg', 'web')

BASE_URL = cfg_p.get_key('HOST')
HEADERS = {
    'Content-type': 'application/json', 
    'Accept': 'text/plain'
}
PERSONS = {}
    
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
            assert_a_person(person)
    global PERSONS
    PERSONS = res

def assert_a_person(person):
    """
    This generic function can be used to assert a single person and all its children.
    """
    assert person['id']
    assert person['timestamp']
    assert person['name']
    assert person['modified']
    traverse(person, assert_persons_con)

def assert_persons_con(node):
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

def test_get_persons_versions():
    """
    Requests /persons/<id>/versions
    """
    for person in PERSONS:
        r = requests.get(BASE_URL + '/persons/%d/versions' % (person['id']), \
            headers=HEADERS)
        res = json.loads(r.text)
        assert r.status_code <= 200
        assert type(res) == type([])
        assert len(res) > 0
        head = res[0]
        assert_a_person(head)

def test_get_person():
    """
    Requests /persons/<id>/versions/<timestamp> and checks for correctness
    """
    for person in PERSONS:
        r = requests.get(BASE_URL + '/persons/%d/versions/%d' % (person['id'], person['timestamp']), \
            headers=HEADERS)
        res = json.loads(r.text)
        assert r.status_code <= 200
        assert type(res) == type({})
        assert_a_person(res)

if __name__ == '__main__':
    """
    Searches for all functions in this module that 
    have the substring 'test' in them and calls them
    """
    current_module = sys.modules[__name__]
    fnList = [f for f in dir(current_module) if 'test' in f]
    map(lambda s: getattr(current_module, s)(), fnList)