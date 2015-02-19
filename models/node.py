class Node():
    def __init__(self, name, lang_code='en', type='c', rel=None, weight=0, edges=[]):
        self.name = name
        self.lang_code = lang_code
        self.type = type
        self.edges = edges
        self.rel = rel
        self.weight = weight

    def __repr__(self):
        """
        Simply returns a dictionary as representation of the object
        """
        return str(self.__dict__)