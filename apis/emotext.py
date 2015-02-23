"""
This module uses a ConceptNet5 REST-API Wrapper to connect to the network.

Given an arbitrary text (that has been stemmed and normalized),
it analyzes every token in order to create a vector that represents
the texts emotions.

This is done by algorithms searching the graph structure of concept net for
connections between a specific token and the entity 'Emotion'.
"""

from models.node import Node
from models.sets import OrderedSet
from math import pow

LANG_TO_CODE = {
    'english': 'en',
    'german': 'de',
    'french': 'fr'
}

MAX_DEPTH = 3

MIN_SCORE = 15

EMOTIONS = set(["love", "anger", "fear", "hate", "happiness", "pleasant", "sadness", "pity", "shame", "ecstasy", "boredom", "love", "cry", "happy", "jealousy", "joy", "surprise", "regret", "frustration", "sorrow", "melancholy", "awe", "fear", "anger", "joy", "orgasm"])

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
    return [build_graph(OrderedSet([Node(t, lang_code, 'c')])) for t in token_list]

def build_graph(queue, depth=0, used_names=OrderedSet([])):
    if depth >= MAX_DEPTH:
        return None
    new_queue = OrderedSet(queue)
    # print ', '.join([e.name for e in new_queue])
    for edge in queue:
        if edge.name in EMOTIONS:
            return {edge.name: calc_nodes_score(edge)}
        else:
            new_queue.remove(edge)
            try:
                edge.edge_lookup(used_names, 'en')
            except:
                continue
            for new_edge in edge.edges:
                if new_edge.name not in used_names and new_edge.score > MIN_SCORE:
                    used_names.add(new_edge.name)
                    new_queue.add(new_edge)
    return build_graph(new_queue, depth+1, used_names)

def calc_nodes_score(node, score=[], score_num=0):
    print node.name + ': %d' % node.score
    if node.parent == None:
        for i, n in enumerate(score):
            score_num = score_num + pow(n, 1/(i+1))
        return score_num
    else:
        score.append(node.score)
        return calc_nodes_score(node.parent, score)

# def build_graph(node, parent_node=None, depth=0, used_names=Set([])):
#     """
#     This function builds a graph structure by doing a lookup on ConceptNet's
#     web-API.

#     For the first call, only a Node object is submitted.
#     Recursively, a further node can be submitted to the function in combination
#     with a parent node to lookup deeper.

#     The function stops, as soon as the MAX_DEPTH constant has passed.
#     """
#     if depth >= MAX_DEPTH:
#         return None
#     # if node.name in EMOTIONS:
#     #     return node
#     used_names.add(node.name)
#     node.edge_lookup(used_names, 'en')
#     for edge in node.edges:
#         if edge.name in EMOTIONS:
#             return edge
#         build_graph(edge, node, depth+1, used_names)
#     return node