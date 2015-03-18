# py.tests starts tests from /test dir, therefore everything further up
# must first be added to its path
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from controllers.sql import PersonCtrl
from controllers.config import CfgParser
from models.models import Person

cfg_p = CfgParser(r'tests/static/test_db.cfg', 'test_db')

print os.path.realpath(__file__)

# static variables
NAME = cfg_p.get_key('NAME')
CONTEXT = {
    cfg_p.get_key('CON_KEY'): cfg_p.get_key('CON_VALUE')
}
SAVED_PERSON = None
DBCTRL = PersonCtrl()


def test_resulttuple_to_obj():
    """
    Tests if a the fetching and conversion of persons from the db is correct.
    """
    persons = DBCTRL.fetchall_persons()
    assert len(persons) > 0 or len(persons) == 0 and type(persons) == type([])
    for p in persons:
        assert p.name
        assert p.id
        assert p.timestamp or p.timestamp == 0    

def test_create_new_person():
    """
    Tests if the creation of a new person in the db yields the right name and types.
    """
    # creation
    new_person = DBCTRL.create_new_person(NAME)
    global SAVED_PERSON
    SAVED_PERSON = new_person

def test_fetch_person():
    """
    Tests is fetching a specific person from the db is correct.
    """
    # fetching
    fetch_persons = DBCTRL.fetchall_persons(lambda x: x.id == SAVED_PERSON.id)
    assert len(fetch_persons) == 1
    fetch_person = fetch_persons[0]
    assert fetch_person.id
    assert fetch_person.name
    assert fetch_person.timestamp or fetch_person.timestamp == 0
    assert fetch_person.id == SAVED_PERSON.id
    assert fetch_person.timestamp == SAVED_PERSON.timestamp
    assert fetch_person.name == SAVED_PERSON.name

def test_delete_person():
    """
    Tests if the previously created person can also be deleted.
    """
    # deletion
    del_person = DBCTRL.delete_person(SAVED_PERSON)
    assert isinstance(SAVED_PERSON, Person) and isinstance(del_person, Person)
    assert type(SAVED_PERSON.id) == type(1) and type(del_person.id) == type(1)
    assert type(SAVED_PERSON.name) == type("") and type(del_person.name) == type("")
    assert type(SAVED_PERSON.timestamp) == type(1) and type(del_person.timestamp) == type(1)
    assert SAVED_PERSON.id == del_person.id
    assert SAVED_PERSON.timestamp == del_person.timestamp
    assert SAVED_PERSON.name == del_person.name

def test_fetch_del_person():
    """
    Tests if it is possible to fetch a deleted person
    """
    # trying to fetch the deleted person
    already_del_persons = DBCTRL.fetchall_persons(lambda x: x.id == SAVED_PERSON.id)
    assert len(already_del_persons) < 1

def test_create_person():
    """
    In contrast to test_create_new_person_and_delete_it this function does not create a 'new'
    person but creates a new version - if you will - for a already existing person.
    """
    person = DBCTRL.create_new_person(NAME)
    person.timestamp += 1
    new_version = DBCTRL.create_person(person)
    assert isinstance(new_version, Person)
    assert new_version.id == person.id
    assert new_version.name == person.name
    assert new_version.timestamp == person.timestamp # this timestamp was incremented above

    # saved in global variable SAVED_PERSON
    global SAVED_PERSON
    SAVED_PERSON = person

def test_create_new_context_for_person():
    """
    Tests is the creation of a new context for a person is possible
    """
    new_context = DBCTRL.create_new_context(CONTEXT.keys()[0], CONTEXT.values()[0], SAVED_PERSON)

def test_create_new_context_for_context():
    """
    Tests is the creation of a new context for a context node is possible
    """
    new_context = DBCTRL.create_new_context(CONTEXT.keys()[0], CONTEXT.values()[0], SAVED_PERSON)

def test_fetch_person_graph():
    graph_person = DBCTRL.fetch_person_graph(Person(None, 63, 'Tim', 1))
    print graph_person

def test_dbctrl_close():
    """
    Tests if a database connection can be closed.
    """
    DBCTRL.close()









