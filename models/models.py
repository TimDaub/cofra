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
            self.id = id
        else:
            raise Exception('Constructor parameters are insufficient.')

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)

class Context():
    """
    Represents a context node in cofra.
    Those can either have a person or another context node as a parent.
    Either one of both must be given, otherwise either the db or this object will yield an error.
    """
    def __init__(self, db_result=None, parent=None, id=None, key=None, value=None):
        # assign parent and if it is not present throw exception
        if parent is not None:
            self.parent = parent
        else:
            raise Exception('Insufficient parameters for Context object.')

        # assign residual parameters
        if db_result:
            self.id = db_result[0]
            self.key = db_result[1]
            self.value = db_result[2]    
        elif id and key and value:
            self.id = id
            self.key = key
            self.value = value
        else:
            raise Exception('Insufficient parameters for Context object.')

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)