# py.tests starts tests from /test dir, therefore everything further up
# must first be added to its path
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from controllers.sql import ContentCtrl
from controllers.config import CfgParser
from models.models import Person

cfg_p = CfgParser(r'tests/static/test_db.cfg', 'test_db')

print os.path.realpath(__file__)

NAME = cfg_p.get_key('NAME')
DBCTRL = ContentCtrl()

def test_resulttuple_to_obj():
    """
    Tests if a the fetching and conversion of persons from the db is correct.
    """
    persons = DBCTRL.fetchall_persons()
    assert len(persons) > 0 or len(persons) and type(persons) == type([])
    for p in persons:
        assert p.name
        assert p.id
        assert p.timestamp or p.timestamp == 0    

def test_create_new_person_and_delete_it():
    """
    Tests if the creation of a new person in the db yields the right name and types.

    and

    Tests is fetching a specific person from the db is correct.

    and

    Tests if the previously created person can also be deleted.

    """

    # creation
    new_person = DBCTRL.create_new_person(NAME)

    # fetching
    fetch_persons = DBCTRL.fetchall_persons(lambda x: x.id == new_person.id)
    assert len(fetch_persons) == 1
    fetch_person = fetch_persons[0]
    assert fetch_person.id
    assert fetch_person.name
    assert fetch_person.timestamp or fetch_person.timestamp == 0

    # deletion
    del_person = DBCTRL.delete_person(new_person)
    assert isinstance(new_person, Person) and isinstance(del_person, Person)
    assert type(new_person.id) == type(1) and type(del_person.id) == type(1)
    assert type(new_person.name) == type("") and type(del_person.name) == type("")
    assert type(new_person.timestamp) == type(1) and type(del_person.timestamp) == type(1)
    assert new_person.name == NAME
    assert del_person.name == NAME

def test_dbctrl_close():
    """
    Tests if a database connection can be closed.
    """
    DBCTRL.close()









