# Emotext

Emotext is framework that helps you extract, saving and correlating emotions with contextual information.
It uses ConceptNet, neo4j and Python for this.

To enable programming-language-indenpendent usage, Emotext's interface is provided as RESTful as possible.

## Installation
Python v2.x is required, as well as `pip` for installing dependencies.
The webserver is hosted using `flask`. Tests are programmed against the RESTful interface, therefore `requests` is needed.


    pip install flask
    pip install requests

Furthermore, `ntlk` is used for natural language processing. It can also be installed using `pip`:

    pip install nltk

However, `ntlk` still needs language-specific files. These can be downloaded by entering the Python IDE:

    >>> import nltk
    >>> nltk.download()

We recommend downloading all dependencies.


docker run -it -p 80:10053 rspeer/conceptnet-web


