from datetime import datetime
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

class Message():
    def __init__(self, entity_name, message, date=datetime.today(), language='english'):
        self.entity_name = entity_name
        self.message = message
        self.date = date
        self.language = language

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)

    def __setitem__(self, key, value):
        self[key] = value

    def process_message_text(self, remove_stopwords=True, stemming=True, remove_punctuation=True, message_tokens=[]):
        """
        Uses NLP functionality as tokenization and stemming from nltk to process the text
        """
        if remove_punctuation:
            punct_tokenizer = RegexpTokenizer(r'\w{2,}')
            message_tokens = punct_tokenizer.tokenize(self.message)
        if len(message_tokens) > 0:
            self.message = " ".join(message_tokens)
        message_tokens = word_tokenize(self.message)
        if stemming: 
            stemmer = SnowballStemmer(self.language, ignore_stopwords=not remove_stopwords)
            message_tokens = [stemmer.stem(t) for t in message_tokens]
        return message_tokens