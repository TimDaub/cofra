from datetime import datetime
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

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

class Person():
    """
    Represents a user in cofra.
    Either db_result or name and timestamp must be given. id doesn't.
    """
    def __init__(self, db_result=None, id=None, name=None, timestamp=None):
        if db_result:
            # order of a result set:
            # id, name, timestamp
            self.id = db_result[0]
            self.name = db_result[1]
            self.timestamp = db_result[2]
        elif name and timestamp:
            self.name = name
            self.timestamp = timestamp
            if id:
                self.id = id
        else:
            raise Exception('Constructor parameters are insufficient.')
