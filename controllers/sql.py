from controllers.config import CfgParser
from models.models import Person
import psycopg2

# Reads configurations from the config.cfg file in root
# and converts them to psycopg2's format:
# http://initd.org/psycopg/docs/module.html#psycopg2.connect
cfg_p = CfgParser(r'config.cfg', 'database')

DATABASE = {
    "DBNAME": cfg_p.get_key('DBNAME'),
    "USER": cfg_p.get_key('USER'),
    "PASSWORD": cfg_p.get_key('PASSWORD'),
    "HOST": cfg_p.get_key('HOST'),
    "PORT": cfg_p.get_key('PORT'),
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
            + DATABASE['USER'] \
            + ":" + DATABASE['PASSWORD'] \
            + "@" + DATABASE['HOST'] \
            + ":" + DATABASE['PORT'] \
            + "/" + DATABASE['DBNAME']
        try:
            self.conn = psycopg2.connect(self.dsn_string)
            # print "Opened database connection"
        except Exception as e:
            print "Opening database connection failed"
            print e

    def close(self):
        """
        Closes the database connection.
        """
        try:
            self.conn.close()
            # print "Closed database connection"
        except Exception as e:
            print "Closing database connection failed"
            print e

class ContentCtrl(PGCtrl):
    """
    Bundles all methods that can be used to manipulate content on the database PGCtrl provides.
    """
    def __init__(self):
        PGCtrl.__init__(self)

    def fetchall_persons(self, filter_fn=None):
        """
        Fetches all persons from the database.
        As parameter, a function can be received that filters certain persons from the
        list being yielded afterwards.
        """
        cur = self.conn.cursor()

        # Get all persons from db
        cur.execute('SELECT id, name, timestamp FROM persons;')
        persons = cur.fetchall()

        # Convert all tuples from result into Person objecs
        persons = self.conv_list_to_obj(persons, Person)

        # if necessary, filter the results for a specific person or group of persons
        if filter_fn is not None:
            persons = filter(filter_fn, persons)
        cur.close()
        return persons

    def create_new_person(self, name):
        """
        A truly new person is created. Essentially this means the primary key 'id' is incremented and
        timestamp is set to zero.
        """
        cur = self.conn.cursor()

        cur.execute('INSERT INTO persons (name, timestamp) VALUES (%s, %s) RETURNING id, name, timestamp;', (name, 0))
        self.conn.commit()
        res = cur.fetchone()
        cur.close()
        return Person(res)

    def create_person(self, person):
        """
        Receives a Person object and inserts it into the db.
        No new person is created, this is just the designated 'update' process.
        """
        cur = self.conn.cursor()

        cur.execute('INSERT INTO persons (id, name, timestamp) VALUES (%s, %s) RETURNING id, name, timestamp;', (person.id, person.name, person.timestamp))
        self.conn.commit()
        cur.close()

    def delete_person(self, person):
        """
        This is just a maintenance function.
        Normally, the data structure implemented is immutable, which means deletions do in fact not happen.
        Therefore, please do not use this function.
        Only in testing this is used.
        """
        cur = self.conn.cursor()

        # execute deletion
        cur.execute('DELETE FROM persons WHERE id = %s AND timestamp = %s RETURNING id, name, timestamp;', (person.id, person.timestamp))

        # and retrieve results
        res = cur.fetchone()

        self.conn.commit()
        cur.close()
        return Person(res)

    def conv_list_to_obj(self, list, obj_class):
        """
        Converts a list of results to a passed in class.
        """
        return [obj_class(res) for res in list]




