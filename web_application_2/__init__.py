from flask import Flask

import pickle 
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import pandas as pd
import re
import ast
from pyemd import emd


app = Flask(__name__)
app.config['SECRET_KEY'] = '740dc2dbaf4e3f6dc1307d8c1f9eee6b'


stop_words = nltk.corpus.stopwords.words('english')

data_web = pd.read_csv('ParsedWebsitesCleanSample.csv')
# data_web = data_web.dropna()
documents_web = data_web.values
print("loading pkl file")
instance_web = pickle.load(open('WordMoverDistance-WebInstanceSLIM.pkl','rb'))

data_blog = pd.read_csv('ParsedBlogsCleanSample.csv')
# data_blog = data_blog.dropna()
documents_blog = data_blog.values
instance_blog = pickle.load(open('WordMoverDistance-BlogInstanceSLIM.pkl','rb'))

def preprocess(doc):
	doc = doc.lower()  # Lower the text.
	doc = word_tokenize(doc)  # Split into words.
	doc = [w for w in doc if not w in stop_words]  # Remove stopwords.
	doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
	return doc


from web_application_2 import templates