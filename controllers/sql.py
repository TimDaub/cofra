from utils.utils import get_config
import psycopg2

# Reads configurations from the config.cfg file in root
# and converts them to psycopg2's format:
# http://initd.org/psycopg/docs/module.html#psycopg2.connect
DATABASE = {
    "database": get_config('database', 'DBNAME'),
    "user": get_config('database', 'USER'),
    "password": get_config('database', 'PASSWORD'),
    "host": get_config('database', 'HOST'),
    "port": get_config('database', 'PORT'),
}

class PGCtrl():
    """
    Bundles all methods that can be used to control a PostgreSQL database.
    """
    def __init__(self):
        """
        Creates a connection string as well as a connection that remains
        open as long as close_con isn't called.
        """
        self.dsn_string = "postgresql://" \
            + get_config('database', 'USER') \
            + ":" + get_config('database', 'PASSWORD') \
            + "@" + get_config('database', 'HOST') \
            + ":" + get_config('database', 'PORT') \
            + "/" + get_config('database', 'DBNAME')
        try:
            self.conn = psycopg2.connect(self.dsn_string)
            print "Opened database connection"
        except Exception as e:
            print "Opening database connection failed"
            print e

    def close_conn(self):
        """
        Closes the database connection.
        """
        try:
            self.conn.close()
            print "Closed database connection"
        except Exception as e:
            print "Closing database connection failed"
            print e

class ContentCtrl(PGCtrl):
    """
    Bundles all methods that can be used to manipulate content on the database PGCtrl provides.
    """
    def __init__(self):
        PGCtrl.__init__(self)

    def fetchall_persons(self):
        """
        Fetches all persons from the database.
        """
        cur = self.conn.cursor()
        cur.execute('SELECT id, name, timestamp FROM persons;')
        persons = cur.fetchall()
        cur.close()
        return persons

    def create_person(self, person):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO persons (name, timestamp) VALUES (%s, %s)', (person.name, person.timestamp))
        self.conn.commit()
        cur.close()




