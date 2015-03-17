from datetime import datetime
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

class Message():
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