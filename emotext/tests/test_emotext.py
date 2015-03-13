import sys
import os.path
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from apis.text import text_processing, calc_percentages

texts = [
    "Hello. This isn't doge! The movie wasn't heavy."
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

def test_calc_percentages():
    emotions = {
        "love": 27.298217235189718,
        "cry": 17.167578907271867,
        "sadness": 8.795877176280856,
        "boredom": 13.366757881808853,
        "frustration": 7.048259470954596,
        "happiness": 12.981467725924063
    }
    calc_percentages(emotions)