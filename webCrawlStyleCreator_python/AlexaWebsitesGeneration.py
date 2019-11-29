from bs4 import BeautifulSoup
import urllib
import re
import csv
import numpy as np
import pandas as pd
import os
import time

def getWebsites(element): #returns True if element is a listed websites
    return re.search('<a href="/siteinfo/', str(element))

def getCategories(element): #returns True if element is a subcategory
    return re.search('<a href="/topsites/category/Top/', str(element))

#getCategoryPath recursively goes through subcategories and runs getWebsitesList only for the deepest subcategories

def getCategoryPath(file_path, current_path, count): 
    print(current_path)
    if count >= 3:
        return
    
    try: #trying to access current url
        htmltext = urllib.request.urlopen("https://www.alexa.com/topsites/category/Top" + current_path).read()
    except: #catches any error in opening current url
        print("Error loading page")
        return current_path
        
    soup = BeautifulSoup(htmltext)

    if soup.find(string=re.compile("No sites for this category.")) != None: #do nothing if the smallest sub-category contains no websites
        return
    texts = soup.findAll(href=True)

    categories_html = filter(getCategories, texts) #contains all categories with some syntax noise
    categories = []

    for text in categories_html: #adds cleaned category string to the categories array
        temp = str(text.encode("utf-8"))
        if current_path == "":
            categories.append(re.search('Top/(.+?)"', temp).group(1))
        else:
            if(re.search(current_path + '/(.+?)"', temp) == None): # skips any URLs with weird characters that produces an error with the regular expression
                continue
            categories.append(re.search(current_path + '/(.+?)"', temp).group(1))
            
    if count == 2 or soup.find(string=re.compile("Sub-Categories \(")) == None: #get the list of top websites of the deepest sub-category
        getWebsitesList(file_path, current_path)                        
    elif count != 2:
        for category in categories: #recurse until it reaches the deepest sub-category
            getCategoryPath(file_path, current_path + "/" + category , count + 1)    
    
    return True


#getWebsitesList inserts top 50 websites of the category_path into csv file

def getWebsitesList(file_path, category_path):
    htmltext = urllib.request.urlopen("https://www.alexa.com/topsites/category/Top" + category_path).read()

    soup = BeautifulSoup(htmltext)
    texts = soup.findAll(href=True)

    websites = filter(getWebsites, texts)
    result = []
    if not os.path.exists(file_path):
        result.append(['website', 'category'])

    for text in websites:
        temp = str(text.encode("utf-8"))
        result.append([re.search('siteinfo/(.+?)"', temp).group(1), category_path])
    result_np = np.asarray(result)

    with open(file_path, 'a') as f:
        if not os.path.exists(file_path):
            pd.DataFrame(result_np).to_csv(f, header=True)
        else:
            pd.DataFrame(result_np).to_csv(f, header=False)
            
            
##Note: Computers, Regional, and Society categories were too big and produced error 503 from Amazon due to the large number of requests. In order to get their datasets, change the count number from 0 to 1
##Note2: Excluded the World category as the sites are not in English

main_categories = ['Adult', 'Arts', 'Business', 'Computers', 'Games', 'Health', 'Home', 'Kids and Teens', 'News', 'Recreation', 'Reference', 'Regional', 'Science', 'Shopping', 'Society', 'Sports']
#main_categories = ['Computers', 'Regional', 'Society'] #have to rerun these with less subcategory depth since there were too many requests to Amazon

for category in main_categories:
    filename = 'websites/alexa_websites_' + category + '.csv' #file path that will contain the csv file
    if os.path.exists(filename):
        os.remove(filename)
    result = getCategoryPath(filename, "/" + category, 1) # Change from count from 0 to 1 for Computers, Regional, and Society categories
    print("Exited recursion with:" + str(result))
    #time.sleep(2) #avoiding error 503 (where amazon blocks access)