# py.tests starts tests from /test dir, therefore everything further up
# must first be added to its path
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from controllers.sql import ContentCtrl
from utils.utils import get_config

NAME = get_config('test_db', 'NAME' 'get', r'tests/static/test_db.cfg')
TIMESTAMP = get_config('test_db', 'TIMESTAMP' 'get', r'tests/static/test_db.cfg')

def test_resulttuple_to_obj():
    """
    Tests if a the fetching and conversion of persons from the db is correct.
    """
    dbctrl = ContentCtrl()
    persons = dbctrl.fetchall_persons()
    assert len(persons) > 0
    for p in persons:
        assert p.name
        assert p.id
        assert p.timestamp or p.timestamp == 0
    dbctrl.close()

def test_fetch_person():
    dbctrl = ContentCtrl()
    persons = dbctrl.fetchall_persons(lambda x: x.id == 1)
    assert len(persons) == 1
    person = persons[0]
    assert person.id
    assert person.name
    assert person.timestamp or person.timestamp == 0
    dbctrl.close()

def test_create_person():
    dbctrl = ContentCtrl()
    dbctrl.create_person(Person(None, None, NAME, ))

    # TODO: How is a person going to get created?