import pytumblr
# pip install pytumblr -- if not already installed
import re, string
# regex to exclude html tag
import datetime as dt

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import json
from zipfile import ZipFile 
import gzip
from datetime import datetime

import pandas as pd
from pandas.io.json import json_normalize

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel

source = argv[1] #'blognames.csv'
keyspace = argv[2] #mcanute

# etl_tumblr_to_cassandra ----------------------------------

# Authenticate via OAuth
# We only need the consumer key to call "posts" function
client = pytumblr.TumblrRestClient('nAvaCgNT6dVls4dxKYnWyM1as57L0aSAkSXAayRCPEtNxJSQjr')

# exclude html tags, punctuation, and extra whitespaces

def reformat_text(data):
    html = re.compile(r'<.*?>')
    temp = html.sub(' ', data)
    special = re.compile(r'[%s\s]+' % re.escape(string.punctuation))
    temp2 = special.sub(' ', temp)
    wspace = re.compile('\s{2,}')
    return wspace.sub(' ', temp2)

def make_json(blogname):
    print(blogname)
    # Make the request
    # Use minkim25.tumblr.com for test
    data = client.posts(blogname + '.tumblr.com')
    
    #To be modified later
    #Filters out all blogs without 'blog' or 'posts' elements
    try:
        website = data['blog']['url']
        last_update = data['posts'][0]['date'][:19]
    except:
        print('Warning: blog or posts or date or url is null')
        return {}
    
    last_update = dt.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
    trail_flag = 0
    
    # Initialization
    title_text = ""
    body_text = ""
    title_font = ""
    body_font = ""
    back_color = ""
    text_color = ""
    link_color = ""   
    
    for post in data['posts']:
        if post['type'] == 'text':
            if trail_flag == 0 and post['trail'] != []:
                theme = post['trail'][0]['blog']['theme']
                title_font = theme['title_font']
                body_font = theme['body_font']
                back_color = theme['background_color']
                text_color = theme['title_color']
                link_color = theme['link_color']
                trail_flag = 1
            if post['title'] != None:
                title_text = title_text + ' ' + post['title']
                title_text = reformat_text(title_text)
            if post['reblog']['comment'] != '':
                body_text = body_text + ' ' + post['reblog']['comment']
                body_text = reformat_text(body_text)
        elif post['type'] == 'photo':
            if trail_flag == 0 and post['trail'] != []:
                theme = post['trail'][0]['blog']['theme']
                title_font = theme['title_font']
                body_font = theme['body_font']
                back_color = theme['background_color']
                text_color = theme['title_color']
                link_color = theme['link_color']
                trail_flag = 1
            title_text = ''
            if post['reblog']['comment'] != '':
                body_text = body_text + ' ' + post['reblog']['comment']
                body_text = reformat_text(body_text)
            
    result = {'website': website, 'last_update': last_update, 'title_font': title_font, 'body_font': body_font, \
              'back_color': back_color, 'text_color': text_color, 'link_color': link_color, \
              'title_text': title_text, 'body_text': body_text}
    return result

# BlogCrawling_blognames ---------------------------------

# Output : Series
# Input : String seed_blog, Series all_sources, Integer recursive_count
# Summary : createSources returns a pandas Series containing blognames that were reblogged by seed_blog without duplicates and NANs
def createSources(seed_blog, all_sources, recursive_count):
    if recursive_count >= total_recursive_count:
        return all_sources
    posts_json = client.posts(seed_blog + '.tumblr.com') #json object with all post information
    if 'posts' in posts_json:
        posts_df = json_normalize(posts_json['posts']) #pandas dataframe
        if 'source_title' in posts_df.columns:
            sources = posts_df['source_title'].dropna().drop_duplicates() #pandas dataframe containing only blognames
            all_sources = all_sources.append(sources)
            for s in sources:
                all_sources = all_sources.append(createSources(s, all_sources, recursive_count + 1)) #recursive call here
    return all_sources.drop_duplicates()

# Output: Series
#Input : Integer total_recursive_count
#Summary: returns list of blognames
def main(total_recursive_count):
    starting_seed = 'adriwong'  #sample initial set-up
    result = createSources(starting_seed, pd.Series([]), 0)
    result.to_csv('Datasources/blognames.csv')

# Authenticate via OAuth
# We only need the consumer key to call "posts" function
client = pytumblr.TumblrRestClient('nAvaCgNT6dVls4dxKYnWyM1as57L0aSAkSXAayRCPEtNxJSQjr')
total_recursive_count = 2 #int(sys.argv[1]) # number of extra layers after the original blog seed !!! ARGV
#main(total_recursive_count)  #assume for now that the set of blogs to get info from will change later so this class isn't needed.


# BlogCrawling_bloginfo --------------------------------------


# Output : Dictionary
# Input : Series sources
# Summary : getPostInfo(sources) runs through sources, which is a pandas Series, and returns a dictionay with the blogname as key and necessary data as value
def getPostInfo(sources):
    info_dict = {}
    for blog in sources:
        try:
            info_dict[blog] = make_json(blog) # make_json is from etl_tumblr_to_cassandra.ipynb
        except:
            '404'
    return info_dict

def main(input_filename, output_filename):
    df = pd.read_csv('Datasources/' + input_filename + '.csv')
    all_sources = df.iloc[:,1]
    s = getPostInfo(all_sources)
    #s = json.dumps(getPostInfo(all_sources))
    #jsonfilename = '/' + output_filename
    #with gzip.open(jsonfilename + ".gz", "wb") as f:
    #    f.write(bytes(s,"utf-8"))

df = pd.read_csv('Datasources/' +source )

all_sources = df.iloc[:,1]
s = getPostInfo(all_sources)

Table = []
for key in s.keys():
    if str(s[key]) != '{}':
        Table.append(pd.io.json.json_normalize(s[key]).values[0]) 

BlogsDF = pd.DataFrame(Table,columns=['back_color' ,'body_font' 	,'body_text' 	,'last_update' 	,'link_color' 	,'text_color' 	,'title_font' 	,'title_text' 	,'website'])

# insert_data_info_cassandra ---------------------------------

cluster = Cluster(['127.0.0.1'])#Cluster(['199.60.17.32','199.60.17.65'])
session = cluster.connect(keyspace)

insert_prepare = "INSERT INTO Blogs(back_color, body_font, body_text, last_update, link_color, text_color, title_font, title_text, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
insert_query = session.prepare(insert_prepare)
# Create batch
batch = BatchStatement()

for index,item in BlogsDF.iterrows():
    if index % 5 == 0:
        session.execute(batch)
        batch.clear()
        batch = BatchStatement()
    batch.add(insert_query,(item.back_color, item.body_font, item.body_text[0:100], datetime.strptime(item.last_update, "%Y-%m-%d %H:%M:%S"), item.link_color, item.text_color, item.title_font, item.title_text, item.website))

print('Done blog info crawling -> loaded into cassandra table Blogs')