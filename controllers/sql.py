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

        This method does not connect persons and their contexts!
        """
        cur = self.conn.cursor()

        # Get all persons from db
        cur.execute("""
            SELECT id, name, MAX(timestamp) as timestamp
            FROM persons 
            GROUP BY id, name;
        """)

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

    def fetch_person_graph(self, person):
        """
        Fetches a specific person and their related contexts.
        Yields a Person object.
        """
        cur = self.conn.cursor()

        # recursively getting all contexts of a person with their id and timestamp
        cur.execute("""
            WITH RECURSIVE ContextsRec (id, key, value, personid, persontimestamp, contextid) 
            AS (
                SELECT init.id, init.key, init.value, init.personid, init.persontimestamp, init.contextid 
                FROM contexts AS init
                WHERE init.personid = %s AND init.persontimestamp = %s

            UNION ALL

                SELECT child.id, child.key, child.value, child.personid, child.persontimestamp, child.contextid
                FROM ContextsRec AS parent, contexts AS child
                WHERE parent.id = child.contextid 
            )
            SELECT id, key, value, personid, persontimestamp, contextid FROM ContextsRec;
        """, (person.id, person.timestamp))

        # Unfortunately, these will yield as a list.
        con_nodes = cur.fetchall()

        # btw: close cursor
        cur.close()

        # But before we build the graph we need to empty the person
        # from eventual children
        person.rmv_children()
        
        # Then, we continue building a graph structure from it.
        return self.build_graph(person, con_nodes)

    def build_graph(self, person, con_nodes):
        """
        Builds a recursive data structure on a person from a list of context nodes.
        Yields a Person object.
        """
        for node in con_nodes:
            # all nodes are resultsets from the db
            # therefore we have to work with indexes
            # A resultset looks like this
            # 
            # (1, 'Polygon', None, 63, 1, None)
            # 
            # and as a schema
            # 
            # (id, key, value, personid, persontimestamp, contextid)
            # 
            # if the node has personid and persontimestamp defined, then we want to add
            # them to the person as a Context obj and delete them from the con_nodes list
            if node[3] or node[3] == 0 and node[4] or node[4] == 0:
                person.add_child(Context(node))
                con_nodes.remove(node)

        return self.build_graph_con_nodes(person, con_nodes)

    def build_graph_con_nodes(self, person, con_nodes):
        """
        Adds all remaining con_nodes to a person's graph.
        Yields a Person object.
        """
        # Once we've added all person-connecting context nodes, we need to continue
        # linking all remaining nodes from the con_nodes list
        # 
        # Algorithm:
        # 1.    If possible, we take the first node in con_nodes = to_insert
        #       Else: There are no further nodes to assign, we return person
        #       
        # 2. Starting at the root of our graph, we traverse it
        #       
        #       either:     until we find to_insert.contextid = trav.id
        #                   if we find the node, then we trav.add_child(to_insert)
        #                   and delete it from con_nodes and start from 1. again
        #       
        #       or:         we're at the end of the tree
        #                   then we move to_insert to the back of con_nodes and start
        #                   from 1. again
        if len(con_nodes) == 0:
            return person
        else:
            to_insert = con_nodes[0]
            # [5] is contextid
            parent_node = self.search_graph(person, to_insert[5])

            if parent_node:
                parent_node.add_child(Context(to_insert))
                con_nodes.remove(to_insert)
            else:
                con_nodes.remove(to_insert)
                con_nodes.append(to_insert)
            # either way, con_nodes are not empty yet, so
            # we need to reiterate once again    
            return self.build_graph_con_nodes(person, con_nodes)

    def search_graph(self, node, id):
        """
        Traverses a tree, looking for an id.
        """
        # Algorithm:
        # If the node has children:
        #   iterate them, check 
        #       if id = child.id then return the child. BINGO!
        #       else: start looking at the child's children
        #       
        # Else the node has no children: return None
        if len(node.children) == 0:
            return None
        else:
            for child in node.children:
                # bingo!
                if child.id == id:
                    return child
                else:
                    return self.search_graph(child, id)

    def create_new_person(self, name):
        """
        A truly new person is created. Essentially this means the primary key 'id' is incremented and
        timestamp is set to zero.
        """
        cur = self.conn.cursor()

        cur.execute(""" 
            INSERT INTO persons (name, timestamp) 
            VALUES (%s, %s) 
            RETURNING id, name, timestamp;
        """, (name, 0))

        self.conn.commit()
        res = cur.fetchone()
        cur.close()
        return Person(res)

    def max_timestamp_person(self, person):
        """
        Gets a person with an id and yields the row with the highest timestamp.
        """
        cur = self.conn.cursor()

        cur.execute("""
            SELECT MAX(timestamp)
            FROM persons 
            WHERE id = %s
        """, [person.id])

        max_timestamp = cur.fetchone()[0]
        cur.close()
        return max_timestamp

    def create_person(self, person):
        """
        Receives a Person object and inserts it into the db.
        No new person is created, this is just the designated 'update' process.
        """
        cur = self.conn.cursor()

        max_timestamp = self.max_timestamp_person(person)

        cur.execute("""
            INSERT INTO persons (id, name, timestamp) 
            VALUES (%s, %s, %s) 
            RETURNING id, name, timestamp;
        """, (person.id, person.name, max_timestamp+1))

        # fetch new version of person
        new_version_person = Person(cur.fetchone())
        new_version_person.add_children(person.children)

        # and update all related children of person
        self.traverse_graph(new_version_person, self.save_and_update_node)
        self.conn.commit()
        cur.close()

        # update person object to map the graph structure
        return self.fetch_person_graph(new_version_person)

    def save_and_update_node(self, parent, child):
        """
        This method can be used in relation with traverse_graph.
        It updates a the child's link to its new parent. 
        """
        cur = self.conn.cursor()
        if isinstance(parent, Person):
            cur.execute("""
                INSERT INTO contexts (key, value, personid, persontimestamp)
                VALUES (%s, %s, %s, %s)
                RETURNING id, key, value, personid, persontimestamp, contextid
            """, (child.key, child.value, parent.id, parent.timestamp))
        elif isinstance(parent, Context):
            cur.execute("""
                INSERT INTO contexts (key, value, contextid)
                VALUES (%s, %s, %s)
                RETURNING id, key, value, personid, persontimestamp, contextid
            """, (child.key, child.value, parent.id))
        else:
            raise Exception('Neither Person nor Context object was used in save_and_update_node to insert content.')

        self.conn.commit()

        # update child and...
        updated_child = Context(cur.fetchone())

        # add his remaining children
        updated_child.add_children(child.children)

        cur.close()
        return updated_child

    def traverse_graph(self, node, fn):
        """
        Traverses a graph and calls a given function on every node it sees on its way.
        """
        if len(node.children) == 0:
            return
        else:
            for child in node.children:
                updated_child = fn(node, child)
                self.traverse_graph(updated_child, fn)
            return

    def delete_person(self, person):
        """ 
        This is just a maintenance function.

        Normally, the data structure implemented is immutable, which means deletions do in fact not happen.
        Therefore, please do not use this function.
        Only in testing, this is used.
        """
        cur = self.conn.cursor()

        # execute deletion
        cur.execute("""
            DELETE FROM persons 
            WHERE id = %s AND timestamp = %s 
            RETURNING id, name, timestamp;
        """, (person.id, person.timestamp))

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
            cur.execute("""
                INSERT INTO contexts (key, value, personid, persontimestamp) 
                VALUES (%s, %s, %s, %s)
                RETURNING id, key, value, personid, persontimestamp;
            """, (key, value, person.id, person.timestamp))

        elif person is None and con_node is not None:
            cur.execute("""
                INSERT INTO contexts (key, value, contextid)
                VALUES (%s, %s, %s)
                RETURNING id, key, value, contextid;
            """, (key, value, con_node.id))
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