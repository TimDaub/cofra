from controllers.config import CfgParser
from models.models import Person
from models.models import Context
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

class PersonCtrl(PGCtrl):
    """
    Bundles all methods that can be used to manipulate a person on the database PGCtrl provides.
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
        cur.execute(""" SELECT id, name, timestamp 
                        FROM persons;""")
        persons = cur.fetchall()

        # Convert all tuples from result into Person objecs
        persons = self.conv_list_to_obj(persons, Person)

        # if necessary, filter the results for a specific person or group of persons
        if filter_fn is not None:
            persons = filter(filter_fn, persons)
        cur.close()
        return persons

    def fet_pers_id_timestamp(self, id, timestamp):
        """
        Convenient little method for fetching a single person with an id and timestamp.
        """
        return self.fetchall_persons(lambda p: p.id == id and p.timestamp == timestamp)[0]

    def create_new_person(self, name):
        """
        A truly new person is created. Essentially this means the primary key 'id' is incremented and
        timestamp is set to zero.
        """
        cur = self.conn.cursor()

        cur.execute(""" INSERT INTO persons (name, timestamp) 
                        VALUES (%s, %s) 
                        RETURNING id, name, timestamp;""", (name, 0))
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

        cur.execute(""" INSERT INTO persons (id, name, timestamp) 
                        VALUES (%s, %s, %s) 
                        RETURNING id, name, timestamp;""", (person.id, person.name, person.timestamp))
        res = cur.fetchone()
        self.conn.commit()
        cur.close()
        return Person(res)

    def delete_person(self, person):
        """
        This is just a maintenance function.
        Normally, the data structure implemented is immutable, which means deletions do in fact not happen.
        Therefore, please do not use this function.
        Only in testing, this is used.
        """
        cur = self.conn.cursor()

        # execute deletion
        cur.execute(""" DELETE FROM persons 
                        WHERE id = %s AND timestamp = %s 
                        RETURNING id, name, timestamp;""", (person.id, person.timestamp))

        # commit results
        self.conn.commit()

         # and retrieve results
        res = cur.fetchone()
        cur.close()
        return Person(res)

    def create_new_context(self, key, value, person=None, con_node=None):
        """
        A contextual information can be added either to a person or another context node.
        Therefore, both person OR con_node can be None.
        This will be checked by a constraint in the DB.
        """            
        cur = self.conn.cursor()
        
        if person is not None and con_node is None:
            cur.execute(""" INSERT INTO contexts (key, value, personid, persontimestamp) 
                            VALUES (%s, %s, %s, %s)
                            RETURNING id, key, value, personid, persontimestamp;""", (key, value, person.id, person.timestamp))
        elif person is None and con_node is not None:
            cur.execute(""" INSERT INTO contexts (key, value, contextid)
                            VALUES (%s, %s, %s)
                            RETURNING id, key, value, contextid;""", (key, value, con_node.id))
        else:
            raise Exception('Insufficient parameters for create_new_context.')

        self.conn.commit()
        res = cur.fetchone()

        # evaluate data from db execution
        # person is used to initialize a Context object later on
        con_person = self.fet_pers_id_timestamp(res[3], res[4])

        cur.close()
        return Context(res, con_person)

    def conv_list_to_obj(self, list, obj_class):
        """
        Converts a list of results to a passed in class.
        """
        return [obj_class(res) for res in list]




