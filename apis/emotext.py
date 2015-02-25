"""
This module uses a ConceptNet5 REST-API Wrapper to connect to the network.

Given an arbitrary text (that has been stemmed and normalized),
it analyzes every token in order to create a vector that represents
the texts emotions.

This is done by algorithms searching the graph structure of concept net for
connections between a specific token and the entity 'Emotion'.
"""
import re

from models.node import Node
from models.sets import OrderedSet

from math import pow

from utils import get_config

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk import pos_tag
from nltk.corpus import wordnet

LANG_TO_CODE = {
    'english': 'en',
    'german': 'de',
    'french': 'fr'
}

MAX_DEPTH = get_config('emotext_graph_search', 'MAX_DEPTH', 'getint')
MIN_WEIGHT = get_config('emotext_graph_search', 'MIN_WEIGHT', 'getint')

EMOTIONS = set(["love", "anger", "fear", "hate", "happiness", "pleasant", "sadness", "pity", "shame", "ecstasy", "boredom", "love", "cry", "happy", "jealousy", "joy", "surprise", "regret", "frustration", "sorrow", "melancholy", "awe", "fear", "anger", "joy"])

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

def text_processing(text, remove_punctuation=True, stemming=True, remove_stopwords=True, language='english', replace_with_antonyms='True'):
    """
    This function enables general text processing.
    It features:
        * Tokenization on sentence level
        * Tokenization on word level
        * Punctuation removal
        * Stemming (and stopword removal)
        * Conversion to lower case
    The language parameter is only required, if stemming and removal of stopwords are desired.
    """

    # Texts often contain punctuation characters.
    # While we'd like to remove them from our data set, their information shouldn't be lost, as
    # it would enable us to handle negation in text later on.
    # 
    # An example:
    # Given the sentence: 'The movie was not bad.', we could convert all
    # adjectives in the sentence to antonyms and remove all negations.
    # Afterwards, the sentence would read 'The movie was good', where 'good'
    # is the antonym of 'bad'.
    # 
    # Therefore, punctuation information should not be lost throughout the process of
    # processing the text with NLP.
    sentence_tokenizer = PunktSentenceTokenizer(PunktParameters())
    # tokenize always returns a list of strings devided by punctuation characters
    # 
    # 'hello' => [u'hello']
    # 'hello. world.' => [u'hello.', u'world.']
    # 
    # Therefore, we need to continue handling a list, namely the sentences variable
    sentences = sentence_tokenizer.tokenize(text)

    # In the english language at least, 
    # there are certain stop words, that introduce low-level negation
    # on a sentence bases.
    # However, these stop words are often melted with their previous verb
    # 
    # isn't = is not
    # wouldn't = would not
    # 
    # This must resolved, as it would not be possible for further functionality of this function to continue
    # extracting information.
    # Especially the 'antonymity' functionality wouldn't work without this
    if language == 'english':
        sw_pattern = r"(n't)"
        sentences = [re.sub(sw_pattern, ' not', s) for s in sentences]
    
    # If desired, the user can no go ahead and remove punctuation from all sentences
    if remove_punctuation:
        # This tokenizer simply removes every character or word which
        # lenght is < 2 and is not a alphabetic one
        punct_rm_tokenizer = RegexpTokenizer(r'\w{2,}')
        # In this case, tokenize will return a list of every word in the sentence
        # 
        # [u'hello'] => [[u'hello']]
        # [u'hello', u'this is another sentence'] => [[u'hello'], [u'this', u'is', u'another', u'sentence']]
        # 
        # Therefore, in the next step we need to handle a list of lists
        sentences = [punct_rm_tokenizer.tokenize(s) for s in sentences]

    # Next, we want to stem on a words basis
    # What this does for example is convert every word into lowercase, remove morphological
    # meanings, and so on.
    if stemming:
        # If desired, stopwords such as 'i', 'me', 'my', 'myself', 'we' can be removed
        # from the text.
        stemmer = SnowballStemmer(language, ignore_stopwords=not remove_stopwords)
        sentences = [[stemmer.stem(w) for w in sentence] for sentence in sentences]
    else:
        # If stemming is not desired, all words are at least converted into lower case
        sentences = [[w.lower() for w in sentence] for sentence in sentences]
        
    return sentences

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
            return {edge.name: calc_nodes_weight(edge)}
        else:
            new_queue.remove(edge)
            try:
                edge.edge_lookup(used_names, 'en')
            except:
                continue
            for new_edge in edge.edges:
                if new_edge.name not in used_names and new_edge.weight > MIN_WEIGHT:
                    used_names.add(new_edge.name)
                    new_queue.add(new_edge)
    return build_graph(new_queue, depth+1, used_names)

def calc_nodes_weight(node, weight=[], weight_num=0):
    print node.name + ': %d' % node.weight
    if node.parent == None:
        for i, n in enumerate(weight):
            weight_num = weight_num + pow(n, 1/(i+1))
        return weight_num
    else:
        weight.append(node.weight)
        return calc_nodes_weight(node.parent, weight)