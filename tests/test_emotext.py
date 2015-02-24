import sys
import os.path
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from apis.emotext import text_processing

texts = [
    "Hello. This is doge! All those punctuation chars should be removed."
]

def test_text_processing():
    """
    Tests:
        * if strings get separated accordingly
        * words contain punctuation chars
        * if there are sentences that have no words.
        * the number of sentences
    """
    sentences = text_processing(texts[0], stemming=False, remove_punctuation=True)
    assert len(sentences) == 3
    for sentence in sentences:
        assert type(sentence) == type([])
        assert len(sentence) > 0
        for w in sentence:
            # check for punctuation characters in word sequence
            assert re.match(r'[^\w]', w) == None