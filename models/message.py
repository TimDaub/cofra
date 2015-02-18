from datetime import datetime

class Message():
    def __init__(self, entity_name, message, date=datetime.today()):
        self.entity_name = entity_name
        self.message = message
        self.date = date

    def __repr__(self):
        return """ 
            name: %s
            message: %s
            date: %s
        """ % (self.entity_name, self.message, str(self.date))