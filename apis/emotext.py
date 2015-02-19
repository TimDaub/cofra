"""
This module uses a ConceptNet5 REST-API Wrapper to connect to the network.

Given an arbitrary text (that has been stemmed and normalized),
it analyzes every token in order to create a vector that represents
the texts emotions.

This is done by algorithms searching the graph structure of concept net for
connections between a specific token and the entity 'Emotion'.
"""

from concept_net_client import lookup
from models.node import Node
from utils import extr_from_concept_net_edge

LANG_TO_CODE = {
    'english': 'en',
    'german': 'de',
    'french': 'fr'
}

def lang_name_to_code(lang_name='english'):
    """
    ConceptNet uses language codes to query words.
    Since we don't want to use those, we've integrated this method
    that allows conversion from language names to language codes.

    If a language code is missing, an exception will be thrown and the user
    will be notified.

    He can furthermore easily adjust the LANG_TO_CODE constant, to add his own language.
    """
    try:
        return LANG_TO_CODE[lang_name]
    except:
        print 'Unfortunately, no lang_code is present for this language.'
        print 'This may be adjusted in apis/emotext.py: LANG_TO_CODE'
        return None

def text_to_emotion(token_list, language='english'):
    """
    This method takes a list of tokes and analyzes every one of those
    by using ConceptNet and a specially implemented graph path search algorithm

    It then returns a vector specifing emotional features of the text.
    """
    lang_code = lang_name_to_code(language)
    if len(token_list) < 1: 
        raise Exception('The token_list must contain at least one word.')
    return [analyze_token(t, lang_code) for t in token_list]

def analyze_token(token, lang_code='en', type='c'):
    """
    Looks up the token on ConceptNet and does a graph search for finding relations
    to any emotions.
    """
    # lookup token via ConceptNet web-API
    token_res = lookup(type, lang_code, token)
    # if result has more than 0 edges continue
    if token_res['numFound'] > 0:
        edges = []
        # for every edge, try converting it to a Node object that 
        # can be processed further
        for e in token_res['edges']:
            # extract basic information from the 'end' key of an edge
            # it contains, type, lang_code and the name of the node
            basic = extr_from_concept_net_edge(e['end'])
            # instantiate a Node object from this information and append it to a list of edges
            edges.append(Node(basic['name'], basic['lang_code'], basic['type'], e['rel'], e['weight'], []))
        # also convert the actual token into a node and add
        # the previously looked up edges to it
        token_node = Node(token, lang_code, type, None, None, edges)
        return token_node
    else:
        # if no edges found on token, raise exception
        raise Exception('Token has no connecting edges.')







