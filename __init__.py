from wsgi.webapp import WSGI
from providers.whatsapp import get_messages

if __name__ == "__main__":
    get_messages(entity_name='Tim')
    WSGI();