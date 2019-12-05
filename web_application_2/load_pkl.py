import pickle 
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import pandas as pd
import re
import ast

stop_words = nltk.corpus.stopwords.words('english')

data_web = pd.read_csv('ParsedWebsitesCleanSample.csv')
data_web = data_web.dropna()
documents_web = data_web.values
instance_web = pickle.load(open('WordMoverDistance-Instance.pkl','rb'))

data_blog = pd.read_csv('ParsedBlogsCleanSample.csv')
data_blog = data_blog.dropna()
documents_blog = data_blog.values
instance_blog = pickle.load(open('WordMoverDistance-BlogInstance.pkl','rb'))

def preprocess(doc):
	doc = doc.lower()  # Lower the text.
	doc = word_tokenize(doc)  # Split into words.
	doc = [w for w in doc if not w in stop_words]  # Remove stopwords.
	doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
	return doc


