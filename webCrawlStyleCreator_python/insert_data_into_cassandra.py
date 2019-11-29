import sys, os, gzip
import json

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel

from datetime import datetime

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+


def main(input_dir, keyspace, table):
    # Read Files
    tumblr_list = readTumblrdata(input_dir, keyspace, table)
    print(tumblr_list)
    
    #Casandra setting
    cluster = Cluster(['199.60.17.32', '199.60.17.65'])
    session = cluster.connect(keyspace)
      
    # Create table
    create_table_prepare = "CREATE TABLE IF NOT EXISTS %s (website TEXT, last_update TIMESTAMP, font_title TEXT, font_body TEXT, color_back TEXT, color_text TEXT, color_link TEXT, text_title TEXT, text_body TEXT, PRIMARY KEY (website))" % (table)
    session.execute(create_table_prepare)      
    
    # Session prepare (INSERT query)
    input_prepare = "INSERT INTO %s (website, last_update, font_title, font_body, color_back, color_text, color_link, text_title, text_body) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)" % (table)      
    insert_query = session.prepare(input_prepare)
    
    # Create batch
    batch = BatchStatement(consistency_level = ConsistencyLevel.QUORUM)
    
    for index, (website, last_update, font_title, font_body, color_back, color_text, color_link, text_title, text_body) in enumerate(tumblr_list):
        if index % 400 == 0:
            session.execute(batch)            
            batch.clear()
            batch = BatchStatement(consistency_level = ConsistencyLevel.QUORUM)                
           
        date_time = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S")
        batch.add(insert_query, (website, last_update, font_title, font_body, color_back, color_text, color_link, text_title, text_body))    

    session.execute(batch)
#End of main()


# Json format
# studioghifli{9}
# website	:	https://studioghifli.tumblr.com/
# last_update	:	2019-07-11 02:08:06
# title_font	:	Gibson
# body_font	:	Helvetica Neue
# back_color	:	#FAFAFA
# text_color	:	#444444
# link_color	:	#529ECC
# title_text	:	
# body_text	:	
def readTumblrdata(input_dir, keyspace, table):
    temp_list = []
    data_list = []

    # Read Files in a directory
    for f in os.listdir(input_dir):
        with gzip.open(os.path.join(input_dir, f), 'rt', encoding='utf-8') as inpuFile:    # Read gzip files
#        with open(input_dir) as inpuFile:    
            lines = json.load(inpuFile)

            for k in lines.keys():
                data = lines.get(k)
                website = data.get('website')            
                if website != None: 
                    temp_list.append(website)
                    temp_list.append(data.get('last_update'))
                    temp_list.append(data.get('title_font'))
                    temp_list.append(data.get('body_font'))
                    temp_list.append(data.get('back_color'))
                    temp_list.append(data.get('text_color'))
                    temp_list.append(data.get('link_color'))
                    temp_list.append(data.get('title_text'))
                    
                    body_text = data.get('body_text')
                    temp_list.append(body_text[:100])             # Do we need body text? 
                    
                    data_list.append(temp_list)
                    temp_list = []
            #End of for loop
    #End of for loop               
    return data_list

#End of readTumblrdata()

    
if __name__ == '__main__':    
    # Default keyspace and table
    casandra_keyspace = "donggul"
    casandra_table = "webcolor_tumblr"  

    # Input check
    if len(sys.argv) < 2:
        print("[Error] Please check input parameters")
        sys.exit(1)        
    elif len(sys.argv) == 3:
        casandra_keyspace = sys.argv[2]
    elif len(sys.argv) > 3:
        casandra_keyspace = sys.argv[2]
        casandra_table = sys.argv[3]  
   
    inputs = sys.argv[1]
    keyspace = casandra_keyspace
    table = casandra_table
    
    print("Path : " + inputs)
    print("keyspace : " + keyspace)
    print("table : " + table)
  
    main(inputs, keyspace, table)
