
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute("CREATE KEYSPACE ColorSchemes WITH REPLICATION = {'class': 'SimpleStrategy','replication_factor':2};")
keyspace = 'ColorSchemes'

session = cluster.connect(keyspace)

createtable = """CREATE TABLE Blogs( 
            back_color TEXT,
            body_font TEXT,
            body_text TEXT,
            last_update TIMESTAMP,
            link_color TEXT,
            text_color TEXT,
            title_font TEXT,
            title_text TEXT,
            website TEXT,
            PRIMARY KEY (website)
            ); """

session.execute(createtable)


