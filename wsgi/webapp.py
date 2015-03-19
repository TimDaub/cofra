import json
from emotext.apis.text import text_to_emotion, text_processing
from flask import Flask
from flask import request
from flask import jsonify
from models.models import Message
from models.models import Person
from emotext.models.models import NodeEncoder
from datetime import datetime
from controllers.sql import PersonCtrl
from models.models import GraphNodeEncoder
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
        message = Message(json_data['entity_name'], json_data['text'], json_data['date'], json_data['language'])
        # process text via Message object method that uses tokenization, stemming, punctuation removal and so on...
        message.text = " ".join([" ".join([w for w in s]) \
                                    for s in \
                                    text_processing(message.text, stemming=False)]) \
                                    .split()
        message_node = text_to_emotion(message.text, message.language)
        # dump processed data back to the client
        return json.dumps(message_node, cls=NodeEncoder, default=default)

    @app.route('/persons', methods=['GET'])
    def get_persons():
        """
        Handles the HTTP request for getting all persons from the db.
        """
        dbctrl = PersonCtrl()
        persons = [dbctrl.fetch_person_graph(p) for p in dbctrl.fetchall_persons(max_timestamp=True)]
        dbctrl.close()
        return json.dumps(persons, cls=GraphNodeEncoder)

    @app.route('/persons/<int:person_id>/versions', methods=['GET'])
    def get_person_versions(person_id):
        """
        Handles the HTTP request for getting a specific persons' versions.
        """
        dbctrl = PersonCtrl()
        persons = dbctrl.fetchall_persons(lambda p: p.id == person_id)
        if len(persons) > 0:
            persons = [dbctrl.fetch_person_graph(p) for p in persons]
            dbctrl.close();
            return json.dumps(persons, cls=GraphNodeEncoder)
        else:
            dbctrl.close()
            return 'No person found with that (id).'

    @app.route('/persons/<int:person_id>/versions/<int:timestamp>', methods=['GET'])
    def get_person(person_id, timestamp):
        """
        Handles the HTTP request for getting one specific person from the db.
        """
        dbctrl = PersonCtrl()
        persons = dbctrl.fetchall_persons(lambda p: p.id == person_id and p.timestamp == timestamp)
        if len(persons) > 0:
            person = dbctrl.fetch_person_graph(persons[0])
            dbctrl.close()
            return json.dumps(person, cls=GraphNodeEncoder)
        else:
            dbctrl.close()
            return 'No person found with that (id, timestamp)'
        





