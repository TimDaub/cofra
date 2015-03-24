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
        """
        Removes all children from the structure.
        """
        self.children = []

    def search_graph(self, id):
        """
        Traverses the structure, looking for an id.
        """
        # Algorithm:
        # If the node has children:
        #   iterate them, check 
        #       if id = child.id then return the child. BINGO!
        #       else: start looking at the child's children
        #       
        # Else the node has no children: return None
        elem = None
        if len(self.children) == 0:
            return None
        else:
            for child in self.children:
                # bingo!
                if child.id == id:
                    elem = child
                else:
                    pot_elem = child.search_graph(id)
                    if pot_elem is not None:
                        elem = pot_elem
            return elem

class GraphNodeEncoder(json.JSONEncoder):
    """
    Taken from: http://stackoverflow.com/a/1458716/1263876

    The GraphNode object is a recursive data structure that can contain itself,
    as it holds all it's child GraphNodes.

    Therefore, this method needs to be defined when trying to serialize a GraphNode object
    to json.
    """
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
           return obj.isoformat()
        if not isinstance(obj, GraphNode):
            return super(GraphNodeEncoder, self).default(obj)
        return obj.__dict__

class Person(GraphNode):
    """
    Represents a user in cofra.
    Either db_res or name and timestamp must be given. id doesn't.
    """
    def __init__(self, db_res=None):
        # Init super class
        GraphNode.__init__(self)

        if db_res:
            # order of a result set:
            self.id = db_res['id']
            self.name = db_res['name']
            self.timestamp = db_res['timestamp']
            if 'modified' in db_res:
                self.modified = db_res['modified']
            else:
                self.modified = None
        else:
            raise Exception('Insufficient parameters for Person object.')

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
    def __init__(self, db_res=None, json_res=None):
        # Init super class
        GraphNode.__init__(self)

        # assign residual parameters
        # id, key, value, modified
        if db_res is not None and json_res is None:
            self.id = db_res['id']
            self.key = db_res['key']
            if 'value' in db_res:
                self.value = db_res['value']
            else:
                self.value = None
            if 'modified' in db_res:
                self.modified = db_res['modified']
            else:
                self.modified = None
        elif json_res is not None and db_res is None:
            self.key = json_res['key']
            if 'value' in json_res and json_res['value'] is not None:
                self.value = json_res['value']
            else:
                self.value = None
        else:
            raise Exception('Insufficient parameters for Context object.')

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)