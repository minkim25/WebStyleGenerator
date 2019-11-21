#!/usr/bin/env python
# coding: utf-8

# In[1]:


## An example of how to run from command line:
##       python BlogCrawling_blognames.py 1
## where 1 is the number of recursion levels
## The output is tumblrdata/blognames.csv file


# In[1]:


import sys
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
import pytumblr
import pandas as pd
from pandas.io.json import json_normalize


# In[3]:


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


# In[8]:


# Output: Series
#Input : Integer total_recursive_count
#Summary: returns list of blognames
def main(total_recursive_count):
    starting_seed = 'adriwong' 
    result = createSources(starting_seed, pd.Series([]), 0)
    result.to_csv('tumblrdata/blognames.csv')


# In[ ]:


# Authenticate via OAuth
# We only need the consumer key to call "posts" function
client = pytumblr.TumblrRestClient('nAvaCgNT6dVls4dxKYnWyM1as57L0aSAkSXAayRCPEtNxJSQjr')
total_recursive_count = int(sys.argv[1]) # number of extra layers after the original blog seed
main(total_recursive_count)

