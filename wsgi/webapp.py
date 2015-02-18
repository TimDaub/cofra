from flask import Flask
app = Flask(__name__)

class WSGI():
    def __init__(self):
        """ Starts the web server and sets up configurations """
        app.debug = True
        app.run()

    @app.route('/entities/<entity_name>', methods=['POST'])
    def read_input_text(entity_name=None):
        return entity_name