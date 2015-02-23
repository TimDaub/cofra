import json
from flask import Flask
from flask import request
from flask import jsonify
from models.message import Message
from models.node import NodeEncoder
from apis.emotext import text_to_emotion
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
        # cast all body data to a Message object
        message = Message(json_data['entity_name'], json_data['message'], json_data['date'], json_data['language'])
        # process text via Message object method that uses tokenization, stemming, punctuation removal and so on...
        message.message = message.process_message_text(stemming=False)
        message_node = text_to_emotion(message.message, message.language)
        # dump processed data back to the client
        return json.dumps(message_node, cls=NodeEncoder)