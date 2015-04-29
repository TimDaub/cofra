 # integration of emotext module
import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../../')

# normal imports, including emotext imports
import json
import dateutil.parser
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from models.models import Person
from models.models import Context
from emotext.models.models import NodeEncoder
from emotext.models.models import Message
from models.et_middleware import Emotext
from datetime import datetime
from controllers.sql import PersonCtrl
from models.models import GraphNodeEncoder
from utils.cronjob import start_cron
from controllers.config import CfgParser
from thread import start_new_thread
from utils.utils import crossdomain
app = Flask(__name__)


cfg_p = CfgParser(r'config.cfg', 'cronjob')

# static vars
CRON_INTERVAL = cfg_p.get_key(key='INTERVAL', method_name='getint')

class WSGI():
    def __init__(self):
        """ Starts the web server and sets up configurations """
        # start the cronjob that looks for decayed rows in the database
        start_new_thread(start_cron, (CRON_INTERVAL,))

        # start the web server
        app.debug = True
        app.run()

    @app.route('/texts', methods=['POST', 'OPTIONS'])
    @crossdomain(origin='*')
    def conv_text():
        """
        Simple method to convert text to a emotion vector, without the structural form of an conversation.
        """
        if request.form.keys() and type(request.form.keys()) == type([]):
            json_data = json.loads(request.form.keys()[0])
        else:
            json_data = request.get_json()

        message = Message('Anonymous', json_data['text'], json_data['date'], json_data['language']).to_emotion_vector()

        data = json.dumps(message.text)
        resp = make_response(data, 200)
        return resp

        
    @app.route('/entities/<entity_name>', methods=['POST'])
    def read_input_text(entity_name=None):
        """
        Handles a POST requests that processes a message json body.
        """

        json_data = request.get_json()
        # cast all body data to a Message object
        message = Message(json_data['entity_name'], json_data['text'], json_data['date'], json_data['language'])
        
        et = Emotext()
        conv = et.handle_message(message)

        if conv is not None:
            resp = jsonify(conv)
        else:
            resp = jsonify({"message": "Message added to cluster algorithm. OK."})
        return resp

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

        Can only create a person without its context.
        If you want to add context to a person look for:

            /persons/<int:person_id>/versions/<int:timestamp>/contexts
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
            return jsonify

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
    def get_specific_person(person_id, timestamp):
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

    @app.route('/persons/<int:person_id>/contexts', methods=['POST'], defaults={'context_id': None})
    @app.route('/persons/<int:person_id>/contexts/<int:context_id>', methods=['POST'])
    def add_context_to_person(person_id, context_id):
        """
        Adds contextual information in form of a node to a person or to another context node to the db.
        """
        data = None
        dbctrl = PersonCtrl()
        post_context = request.get_json()
        persons = dbctrl.fetchall_persons(filter_fn=lambda p: p.id == person_id, max_timestamp=True)
        if len(persons) > 0:

            # initialize both the person and the context object
            person = dbctrl.fetch_person_graph(persons[0])
            new_context = Context(json_res=post_context)

            # decide on the submitted context nodes parent
            if context_id or context_id == 0:
                parent_node = person.search_graph('id', context_id)
                parent_node.add_child(new_context)
            else:
                person.add_child(new_context)
            
            # create new version of the original person
            new_version = dbctrl.create_person(person)
            data = json.dumps(new_version, cls=GraphNodeEncoder)
            dbctrl.close()
            return make_response(data, 200)
        else:
            dbctrl.close()
            data = 'No person found with that (id, timestamp)'
            return make_response(data, 400)

    @app.route('/persons/<int:person_id>/contexts/<int:context_id>', methods=['DELETE'])
    def remove_context_from_person(person_id, context_id):
        """
        Removes a context node from a person and creates a new version of it.
        """
        data = None
        dbctrl = PersonCtrl()
        persons = dbctrl.fetchall_persons(filter_fn=lambda p: p.id == person_id, max_timestamp=True)
        if len(persons) > 0:
            person = dbctrl.fetch_person_graph(persons[0])
            node_to_remove = person.rmv_graph_child(context_id)
            if node_to_remove is not None:
                new_version = dbctrl.create_person(person)
                data = json.dumps(new_version, cls=GraphNodeEncoder)
                dbctrl.close()
                return make_response(data, 200)
            else:
                data = 'No context node found with that (id)'
                dbctrl.close()
                return make_response(data, 400)
            
        else:
            dbctrl.close()
            data = 'No person found with that (id, timestamp)'
            return make_response(data, 400) 

