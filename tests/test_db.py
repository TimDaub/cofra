# py.tests starts tests from /test dir, therefore everything further up
# must first be added to its path
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from controllers.sql import PersonCtrl
from controllers.config import CfgParser
from models.models import Person
from models.models import Context
from collections import Counter

cfg_p = CfgParser(r'tests/static/test_db.cfg', 'db')

# static variables
NAME = cfg_p.get_key('NAME')

CONTEXTS = [{
    "key": cfg_p.get_key('CON_KEY'),
    "value": cfg_p.get_key('CON_VALUE')
},
{
    "key": cfg_p.get_key('CON_KEY2'),
    "value": cfg_p.get_key('CON_VALUE2')
}]

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
    del_persons = DBCTRL.delete_person(SAVED_PERSON)
    for person in del_persons:
        assert isinstance(SAVED_PERSON, Person) and isinstance(person, Person)
        assert type(SAVED_PERSON.id) == type(1) and type(person.id) == type(1)
        assert type(SAVED_PERSON.name) == type("") and type(person.name) == type("")
        assert type(SAVED_PERSON.timestamp) == type(1) and type(person.timestamp) == type(1)
        assert SAVED_PERSON.id == person.id
        assert SAVED_PERSON.name == person.name

def test_fetch_del_person():
    """
    Tests if it is possible to fetch a deleted person.
    """
    # trying to fetch the deleted person
    already_del_persons = DBCTRL.fetchall_persons(lambda x: x.id == SAVED_PERSON.id)
    assert len(already_del_persons) < 1

def test_create_person():
    """
    In contrast to test_create_new_person and test_delete_person this function does not create a 'new'
    person but creates a new version - if you will - for a already existing person.
    """
    person = DBCTRL.create_new_person(NAME)
    new_version = DBCTRL.create_person(person)
    assert isinstance(new_version, Person)
    assert new_version.id == person.id
    assert new_version.name == person.name
    assert new_version.timestamp == person.timestamp+1 # this timestamp was incremented above

    # saved in global variable SAVED_PERSON
    global SAVED_PERSON
    SAVED_PERSON = new_version

def test_fetch_person_graph():
    """
    Fetches a full graph structured person from the database.
    """
    global SAVED_PERSON
    graph_person = DBCTRL.fetch_person_graph(SAVED_PERSON)
    SAVED_PERSON = graph_person

def test_add_context_to_person():
    """
    Adds a context node to a person.
    """
    global SAVED_PERSON
    global CONTEXTS
    con = Context(json_res=CONTEXTS[0])
    # test instantiation of a Context object
    assert isinstance(con, Context)
    assert con.key
    assert type(con.children) == type([])
    
    # test adding the Context Object to a person
    SAVED_PERSON.add_child(con)
    # and save this person to the database
    new_version = DBCTRL.create_person(SAVED_PERSON)

    # unfortunately we never know the sure id of the context
    # node we recently created, but we can be almost sure by 
    # comparing ids of graph searches with different properties
    con_ids = list()

    # testing new version of the person
    assert SAVED_PERSON.timestamp+1 == new_version.timestamp
    assert SAVED_PERSON.id == new_version.id
    key_con = new_version.search_graph('key', con.key)
    assert key_con
    con_ids.append(key_con.id)
    if con.value is not None:
        value_con = new_version.search_graph('value', con.value)
        assert value_con
        con_ids.append(value_con.id)
    if con.decay is not None:
        decay_con = new_version.search_graph('decay', con.decay)
        assert decay_con
        con_ids.append(decay_con.id)
    assert len(con_ids) > 0
    most_common_id = Counter(con_ids).most_common(1)[0][0]
    CONTEXTS.append(new_version.search_graph('id', most_common_id))
    SAVED_PERSON = new_version

def test_add_context_to_context():
    """
    Adds a context node to a context node.
    """
    con_ids = list()
    parent_con = CONTEXTS[-1]
    con_to_add = Context(json_res=CONTEXTS[1])
    parent_con.add_child(con_to_add)
    new_version = DBCTRL.create_person(SAVED_PERSON)

    # testing values of new version
    assert SAVED_PERSON.timestamp+1 == new_version.timestamp
    assert SAVED_PERSON.id == new_version.id
    key_con = new_version.search_graph('key', con_to_add.key)
    assert key_con
    con_ids.append(key_con.id)
    if con_to_add.value is not None:
        value_con = new_version.search_graph('value', con_to_add.value)
        assert value_con
        con_ids.append(value_con.id)
    if con_to_add.decay is not None:
        decay_con = new_version.search_graph('decay', con_to_add.decay)
        assert decay_con
        con_ids.append(decay_con.id)
    counted_ids = Counter(con_ids).most_common(1)
    assert len(counted_ids) == 1
    test_delete_person()

def test_dbctrl_close():
    """
    Tests if a database connection can be closed.
    """
    DBCTRL.close()









