"""
This module uses a ConceptNet5 REST-API Wrapper to connect to the network.

Given an arbitrary text (that has been stemmed and normalized),
it analyzes every token in order to create a vector that represents
the texts emotions.

This is done by algorithms searching the graph structure of concept net for
connections between a specific token and the entity 'Emotion'.
"""

from models.node import Node

LANG_TO_CODE = {
    'english': 'en',
    'german': 'de',
    'french': 'fr'
}

MAX_DEPTH = 2

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
    return [build_graph(Node(t, lang_code, 'c')) for t in token_list]

def build_graph(node, parent_node=None, depth=0):
    """
    This function builds a graph structure by doing a lookup on ConceptNet's
    web-API.

    For the first call, only a Node object is submitted.
    Recursively, a further node can be submitted to the function in combination
    with a parent node to lookup deeper.

    The function stops, as soon as the MAX_DEPTH constant has passed.
    """
    if depth >= MAX_DEPTH:
        return None
    node.edge_lookup()
    for edge in node.edges:
        build_graph(edge, node, depth+1)
    return node