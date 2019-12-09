

from bs4 import BeautifulSoup
import urllib, random, re, string
import cssutils
from pprint import pprint
import numpy as np
import pandas as pd
from pandas.io.formats.style import Styler
import nltk
import sys
import re
import pickle

nltk.download('words')
words = set(nltk.corpus.words.words())

infile = open('otherwords.pkl','rb')
otherWordsNotWanted = pickle.load(infile)
infile.close()


inputs = sys.argv[1] #'alexa_websites_All.csv'
start =  sys.argv[2] #0 
end = sys.argv[3] #3 




def visible(element):
   #if element.parent.name in [ 'script', '[document]', 'head', 'title','style']:
   if element.parent.name in ['[document]', 'script', 'head', 'title']:
       return False
   elif re.match('<!--.*-->', str(element)):
       return False
   return True


def isAboutPage(element):
    if 'about' in element:
        return True
    return False


def websiteText(url):
    htmltext = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(htmltext)
    texts = soup.findAll(text=True)
    visible_texts = filter(visible, texts)
    result = filter(lambda x: x != '\n', visible_texts)
    articleResult = ""
 
    for text in result:
        articleResult += str(text.encode("utf-8"))
 
    articleResult = str(articleResult)
    #articleResult = BeautifulSoup(articleResult, convertEntities=BeautifulSoup.HTML_ENTITIES)
 
    return articleResult


# In[20]:


def getAllHrefs(url):
    hrefs = []
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page)
 
    for link in soup.findAll('a'):
        href = link.get('href')
 
        if href[0] == '/' :
            href = url + href
        hrefs.append(href)    
 
    return hrefs


# # Semantic Text


def getAboutPages(url):
    allHrefs = getAllHrefs(url)
 
    aboutPages = filter(isAboutPage, allHrefs)
    return aboutPages
        

def removeNonWords(text):
    text =  " ".join(x for x in nltk.wordpunct_tokenize(text) if x.lower() in words or not x.isalpha())
    for otherWord in otherWordsNotWanted:
        text = re.sub(otherWord, '', text)

    text =  " ".join(x for x in nltk.wordpunct_tokenize(text) if x.lower() in words or not x.isalpha())

    return text


# # Style Text


def isProperHex(t):
    return bool(re.search('[A-Fa-f0-9]{6}', t))


def onlyColour(t):
    startPos = t.find('#')
    return t[startPos:startPos+8]



def getStylePages(url):
    htmltext = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(htmltext)
    cssSheets = [link["href"] for link in soup.findAll('link') if 'stylesheet' in link.get('rel', [])]
    
    return [sheet for sheet in cssSheets if ('//' not in sheet or 'https://' in sheet)] 


def getFonts(url, top=3):
    
    fonts = []
    cssPagesSample = getStylePages(url)
    cssPages = list(cssPagesSample)
    
    for cssPage in cssPages:
        if cssPage[0:4]=='http':
            styleSample = cssPage
        else:
            styleSample = url+cssPage
            
        cssText = urllib.request.urlopen(styleSample).read()
        soup = BeautifulSoup(cssText)
        cssTextRaw = soup.findAll(text=True)
        
        if cssTextRaw == []:
            break
        
        for styletag in str(cssTextRaw[0]).split('}'):
            if 'font-family' in styletag:
                startPos = styletag.find('font-family')
                endPos = styletag.find(';',startPos)
                fonts.append(styletag[startPos:endPos])
                
    
    fonts = np.array(fonts)
    unique, counts = np.unique(fonts, return_counts=True)
    
    df = pd.DataFrame(np.asarray((unique, counts)).T,columns=['Font','Count'])
    df = df.sort_values(by='Count',ascending=False).head(top)
    
    return df

def getBackgroundColors(url, top=3, renderColor = True):
    
    backgroundColors = []
    cssPagesSample = getStylePages(url)
    cssPages = list(cssPagesSample)
    
    #print(cssPages)
    
    for cssPage in cssPages:
        if cssPage[0:4]=='http':
            styleSample = cssPage
        else:
            styleSample = url+cssPage
            
        cssText = urllib.request.urlopen(styleSample).read()
        soup = BeautifulSoup(cssText)
        cssTextRaw = soup.findAll(text=True)
        
        #print(cssTextRaw )
        
        if cssTextRaw == []:
            break
        for styletag in str(cssTextRaw[0]).split('}'):
            if 'background-color' in styletag:
                startPos = styletag.find('background-color')
                endPos = styletag.find(';',startPos)
                backgroundColors.append(styletag[startPos:endPos])
    
    bgColors = np.array(backgroundColors)
    unique, counts = np.unique(bgColors, return_counts=True)
    
    df = pd.DataFrame(np.asarray((unique, counts)).T,columns=['Colour','Count'])
    df['IsProper'] = df['Colour'].apply(isProperHex)
    df = df[df['IsProper']==True]
    df['Colour'] = df['Colour'].apply(onlyColour)
    df['Count'] = df['Count'].apply(lambda x : int(x))
    df = df.drop(['IsProper'],axis=1)
    
    df = df.sort_values(by='Count',ascending=False).head(top)
    
    if renderColor:
        return df.style.applymap(lambda x:"background-color: %s"%x, subset=['Colour']) 
    else:
        return df

def websiteAboutTextOrMainPage(url):
    try: 
        abouts = getAboutPages(url)
        text = ""
        for about in abouts:
            text = text + ' ' + websiteText(about)
            
        text = removeNonWords(text)
    except:
        try:
            text = websiteText(url)
            text = removeNonWords(text)
        except:
            return '404 could not reach site'
    return text[0:8000]

df = pd.read_csv(inputs)


Table = []


Row = []


for row in df.values[int(start):int(end)]:
    if row[0] % 100 == 0:
        print(row[0],str(row[1]))
    Row.append(row[1])
    Row.append(row[2])
    
    try:
        colors = getBackgroundColors('https://www.'+row[1]+'/',3,False).values
    except:
        colors = []
    Row.append(colors)
    
    try:
        fonts = getFonts('https://www.'+row[1]+'/',3).values
    except:
        fonts = []
    Row.append(fonts)
    
    text = websiteAboutTextOrMainPage('https://www.'+row[1]+'/')
    Row.append(text)
    
    Table.append(Row)
    Row = []


pd.DataFrame(Table,columns=['Website','WebsiteCategory','Colors','Fonts','Text']).to_csv('alexa_websites_'+str(start)+'_'+str(end)+'.csv')



