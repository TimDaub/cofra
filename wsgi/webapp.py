import json
from emotext.apis.text import text_to_emotion, text_processing
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from models.models import Message
from models.models import Person
from emotext.models.models import NodeEncoder
from datetime import datetime
from controllers.sql import PersonCtrl
from models.models import GraphNodeEncoder
import dateutil.parser
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
        data = json.dumps(persons, cls=GraphNodeEncoder)
        return make_response(data, 200)

    @app.route('/persons', methods=['POST'])
    def post_person():
        """
        Handles the HTTP request for posting/creating a person to the db.
        """
        dbctrl = PersonCtrl()
        post_person = request.get_json()
        if 'name' in post_person and post_person['name'] is not None:
            new_person = dbctrl.create_new_person(post_person['name'])
            dbctrl.close()
            data = json.dumps(new_person, cls=GraphNodeEncoder)
            return make_response(data, 201)
        else:
            data = 'Specify name in body'
            return make_response(data, 400)

    @app.route('/persons/<int:person_id>/versions', methods=['GET'])
    def get_person_versions(person_id):
        """
        Handles the HTTP request for getting a specific persons' versions.
        """
        fetch_filter = None
        start_datetime = None
        end_datetime = None
        # This route can be requested using a querystring for selecting a 
        # person for a specific datetime range.
        # The parameters for this procedure are 'start_datetime' and 'end_datetime'
        # 
        # datetimes can only be sent in 'isoformat', which is: YYYY-MM-DDTHH:MM:SS.mmmmmm
        
        if request.args.get('startdatetime'):
            start_datetime = dateutil.parser.parse(request.args.get('startdatetime'))
        if request.args.get('enddatetime'):
            end_datetime = dateutil.parser.parse(request.args.get('enddatetime'))

        if start_datetime and end_datetime:
            fetch_filter = lambda p: p.id == person_id and p.modified > start_datetime and p.modified < end_datetime
        elif start_datetime:
            fetch_filter = lambda p: p.id == person_id and p.modified > start_datetime
        elif end_datetime:
            fetch_filter = lambda p: p.id == person_id and p.modified < end_datetime
        else:
            fetch_filter = lambda p: p.id == person_id

        dbctrl = PersonCtrl()
        persons = dbctrl.fetchall_persons(fetch_filter)
        if len(persons) > 0:
            persons = [dbctrl.fetch_person_graph(p) for p in persons]
            dbctrl.close();
            data = json.dumps(persons, cls=GraphNodeEncoder)
            return make_response(data, 200)
        else:
            dbctrl.close()
            data = 'No person found with that (id)'
            return make_response(data, 200)

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
            data = json.dumps(person, cls=GraphNodeEncoder)
            return make_response(data, 200)
        else:
            dbctrl.close()
            data = 'No person found with that (id, timestamp)'
            return make_response(data, 400)
        





