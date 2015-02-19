import json
from flask import Flask
from flask import request
from models.message import Message
from datetime import datetime
app = Flask(__name__)

class WSGI():
    def __init__(self):
        """ Starts the web server and sets up configurations """
        app.debug = True
        app.run()

    @app.route('/entities/<entity_name>', methods=['POST'])
    def read_input_text(entity_name=None):
        """
        Handles a POST requests that processes a message json body.
        """
        json_data = request.get_json()
        # cast all body data to Message object
        message = Message(json_data['entity_name'], json_data['message'], datetime.strptime(json_data['date'], '%Y-%m-%dT%H:%M:%S'), json_data['language'])
        # process text via Message object method that uses tokenization, stemming, punctuation removal and so on...
        message.message = message.process_message_text()
        print message
        return entity_name