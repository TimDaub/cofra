from datetime import datetime
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import json

class Message():
    """
    Represents a message a user of Emotext sends to the cofra framework.
    """
    def __init__(self, entity_name, text, date=datetime.today(), language='english'):
        self.entity_name = entity_name
        self.text = text
        self.date = date
        self.language = language

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)

    def __setitem__(self, key, value):
        self[key] = value

class GraphNode():
    """
    Represents a node in a graph.
    """
    def __init__(self):
        self.children = []

    def add_child(self, child):
        """
        Adds a child node to the nodes's children.
        """
        if isinstance(child, Context):
            self.children.append(child)
        else:
            # Since a Person object is always the root node, only Context objects
            # can ever be added to the graph structure as children.
            raise Exception('Only Context objects can be added to a graph.')

    def rmv_child(self, child):
        """
        Removes a child node from a nodes's children.
        """
        self.children.remove(child)

    def add_children(self, children):
        """
        Adds a list of children to the graph.
        Uses the add_child method.
        """
        for child in children:
            self.add_child(child)

    def rmv_children(self):
        self.children = []

class GraphNodeEncoder(json.JSONEncoder):
    """
    Taken from: http://stackoverflow.com/a/1458716/1263876

    The GraphNode object is a recursive data structure that can contain itself,
    as it holds all it's child GraphNodes.

    Therefore, this method needs to be defined when trying to serialize a GraphNode object
    to json.
    """
    def default(self, obj):
        if not isinstance(obj, GraphNode):
            return super(GraphNodeEncoder, self).default(obj)
        return obj.__dict__

class Person(GraphNode):
    """
    Represents a user in cofra.
    Either db_result or name and timestamp must be given. id doesn't.
    """
    def __init__(self, db_result=None, id=None, name=None, timestamp=None):
        # Init super class
        GraphNode.__init__(self)

        if db_result:
            # order of a result set:
            # id, name, timestamp
            self.id = db_result[0]
            self.name = db_result[1]
            self.timestamp = db_result[2]
        elif name and timestamp:
            self.name = name
            self.timestamp = timestamp
            self.id = id
        else:
            raise Exception('Constructor parameters are insufficient.')

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)

class Context(GraphNode):
    """
    Represents a context node in cofra.

    'value' can be None.
    """
    def __init__(self, db_result=None, id=None, key=None, value=None):
        # Init super class
        GraphNode.__init__(self)

        # assign residual parameters
        if db_result:
            self.id = db_result[0]
            self.key = db_result[1]
            if db_result[2]:
                self.value = db_result[2]
            else:
                self.value = None 
        elif id and key:
            self.id = id
            self.key = key
            if value:
                self.value = value
            else:
                self.value = None
        else:
            raise Exception('Insufficient parameters for Context object.')

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)