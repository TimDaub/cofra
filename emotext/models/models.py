import json
from ..apis.concept_net_client import lookup
from ..utils.utils import extr_from_concept_net_edge

class Node():
    def __init__(self, name, lang_code='en', type='c', rel=None, weight=0, edges=[], parent=None):
        self.name = name
        self.lang_code = lang_code
        self.type = type
        self.edges = edges
        self.rel = rel
        self.weight = weight
        self.parent = parent

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)

    def edge_lookup(self, used_names, lang_code='en'):
        """
        Uses ConceptNet's lookup function to search for all related
        nodes to this one.

        Subsequently parses all of those edges and returns nothing
        when update was successful.
        """
        # node must at least have a name to do a lookup
        # otherwise, an exception is raised
        if self.name == None:
            raise Exception('Cannot do edge_lookup without nodes name.')
        # lookup token via ConceptNet web-API
        req = lookup(self.type, self.lang_code, self.name)
        token_res = req
        # used_names is a list of objects, however, in order to perform lookups,
        # we need it to be a list of strings
        # if result has more than 0 edges continue
        if token_res != None and token_res['numFound'] > 0:
            edges = []
            # for every edge, try converting it to a Node object that 
            # can be processed further
            for e in token_res['edges']:
                # extract basic information from the 'end' key of an edge
                # it contains, type, lang_code and the name of the node
                basic_start = extr_from_concept_net_edge(e['start'])
                basic_end = extr_from_concept_net_edge(e['end'])
                # instantiate a Node object from this information and append it to a list of edges
                # print basic_start['name'] + ' --> ' + e['rel'] + ' --> ' + basic_end['name']
                if basic_end['name'] != self.name:
                    if basic_end['name'] not in used_names and basic_end['lang_code'] == lang_code:
                        edges.append(Node(basic_end['name'], basic_end['lang_code'], basic_end['type'], e['rel'], e['weight'], [], self))
                else:
                    if basic_start['name'] not in used_names and basic_start['lang_code'] == lang_code:
                        edges.append(Node(basic_start['name'], basic_start['lang_code'], basic_start['type'], e['rel'], e['weight'], [], self))
            # if all edges have been processed, add them to the current object
            self.edges = edges
        else:
            # if no edges found on token, raise exception
            raise Exception('Token has no connecting edges.')

class NodeEncoder(json.JSONEncoder):
    """
    Taken from: http://stackoverflow.com/a/1458716/1263876

    The Node object is a recursive data structure that can contain itself,
    as it holds all it's child Nodes.

    Therefore, this method needs to be defined when trying to serialize a Node object
    to json.
    """
    def default(self, obj):
        if not isinstance(obj, Node):
            return super(NodeEncoder, self).default(obj)

        return obj.__dict__
