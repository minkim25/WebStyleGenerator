#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## An example of how to run from command line:
##       ipython BlogCrawling_bloginfo.py blognames output_filename
## where output_filename is the output zip file name
## The output is tumblrdata/output_filename.gz
## Make sure to run it with ipython and not python


# In[ ]:


get_ipython().run_line_magic('run', 'etl_tumblr_to_cassandra.ipynb')

import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import json
from zipfile import ZipFile 
import gzip
import pandas as pd


# In[ ]:


# Output : Dictionary
# Input : Series sources
# Summary : getPostInfo(sources) runs through sources, which is a pandas Series, and returns a dictionay with the blogname as key and necessary data as value
def getPostInfo(sources):
    info_dict = {}
    for blog in sources:
        info_dict[blog] = make_json(blog) # make_json is from etl_tumblr_to_cassandra.ipynb
    return info_dict


# In[ ]:


def main(input_filename, output_filename):
    df = pd.read_csv('tumblrdata/' + input_filename + '.csv')
    all_sources = df.iloc[:,1]
    s = json.dumps(getPostInfo(all_sources))
    jsonfilename = 'tumblrdata/' + output_filename
    with gzip.open(jsonfilename + ".gz", "wb") as f:
        f.write(bytes(s,"utf-8"))


# In[ ]:


input_filename = sys.argv[1]
output_filename = sys.argv[2]
main(input_filename, output_filename)

