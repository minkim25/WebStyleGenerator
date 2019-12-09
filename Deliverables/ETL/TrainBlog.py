from gensim.models import KeyedVectors

from gensim.models import KeyedVectors

model2 = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin.gz', binary=True)
import pandas as pd
import nltk
from gensim.similarities import WmdSimilarity
import pickle
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
cluster = Cluster(['127.0.0.1'])#Cluster(['199.60.17.32','199.60.17.65'])
session = cluster.connect('mcanute')

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import download
stop_words = stopwords.words('english')
import gensim
from nltk import word_tokenize
nltk.download('punkt')  # Download data for tokenizer.

def preprocess(doc):
    doc = doc.lower()  # Lower the text.
    doc = word_tokenize(doc)  # Split into words.
    doc = [w for w in doc if not w in stop_words]  # Remove stopwords.
    doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
    return doc
from pyemd import emd

query = "SELECT * from Blogs;"
data = pd.DataFrame(list(session.execute(query)))

data = data.dropna() 
data = data[data['body_text'].apply(len)>2]
documents = data.values
wmd_corpus = data['body_text'].apply(preprocess).values
instance = WmdSimilarity(wmd_corpus, model2, num_best=3)
pickle.dump(instance,open('WordMoverDistance-BlogInstanceSLIM.pkl','wb'))
