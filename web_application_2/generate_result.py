import pickle 
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import pandas as pd
import re
import ast

# from web_application import app
from web_application_2 import stop_words, documents_web, instance_web, preprocess
from web_application_2 import documents_blog, instance_blog


# this function is for post-development of "popular topic" option
def regex_text(val):
	if val:
		reg = re.compile(r'\b\w{3,20}\b')
		temp = reg.findall(val)
		temp_set = set(temp)
		temp_list = list(temp_set)
		if len(temp_list) < 20:
		    temp2 = temp_list
		elif len(temp_list) < 50:
		    temp2 = temp_list[10:]
		elif len(temp_list) < 100:
		    temp2 = temp_list[30:]
		else:
		    temp2 = temp_list[50:100]
		result = " ".join(temp2) 
		return ("..." + result + "....")
	else:
		return "Empty string found"


def similarityWeb(description):  
	description = description.replace('data', '')
	print('running query')
	query = preprocess(description)
	sims = instance_web[query]  # A query is simply a "look-up" in the similarity class.

	# Print the query and the retrieved documents, together with their similarities.
	results = []
	print(description)
	for i in range(3):

		row = []
		try:
			row.append(documents_web[sims[i][0]][0]) # WebsiteKey
			row.append(documents_web[sims[i][0]][2]) # Website
			row.append(documents_web[sims[i][0]][3]) # Colors
			row.append(documents_web[sims[i][0]][4]) # Fonts
			row.append(documents_web[sims[i][0]][5]) # Text
			row.append(sims[i][1])    # Similarity
			results.append(row)
		except IndexError:
			row.append("sampleWebsiteKey") # WebsiteKey
			row.append("sampleWebsite") # Website
			row.append([['#FFFFFF', 1],['#FFFFFF', 1],['#FFFFFF', 1]]) # Colors
			row.append([['font-family:Arial', '1'],['font-family:Arial', '1'],['font-family:Arial', '1']]) # Fonts
			row.append("sampleText") # Text
			row.append("0.0")    # Similarity
			results.append(row)
			break

		results.append(row)
	resultsDF = pd.DataFrame(results)
	#resultsDF.to_csv(description + '.csv')

	resultsDF.columns = ['WebsiteKey','Website','Colours','Fonts','Text','Similarity']
	resultsDF['Fonts'] = resultsDF['Fonts'].replace({'\" \'': '\", \'', "\' \'": "\', \'", '(\r\n)': ','}, regex=True)
	resultsDF['Colours'] = resultsDF['Colours'].replace({' ': ', '}, regex=True)
	resultsDF['Text'] = resultsDF['Text'].apply(regex_text)
	resultsDF = resultsDF.sort_values(by=['Similarity'],ascending=False)
	return resultsDF#.style.set_properties(subset=['Text'], **{'width': '350px'})

def similarityBlog(description):  
	description = description.replace('data', '')
	query = preprocess(description)
	sims = instance_blog[query]  # A query is simply a "look-up" in the similarity class.

	# Print the query and the retrieved documents, together with their similarities.
	results = []
	for i in range(4):

		row = []
		try:
			row.append(documents_blog[sims[i][0]][1]) # Website
			row.append(documents_blog[sims[i][0]][2]) # Back_Color
			row.append(documents_blog[sims[i][0]][6]) # Link_Color
			row.append(documents_blog[sims[i][0]][7]) # Text_Color
			row.append(documents_blog[sims[i][0]][8]) # Title_Font
			row.append(documents_blog[sims[i][0]][3]) # Body_Font
			row.append(documents_blog[sims[i][0]][4]) # Text
			row.append(sims[i][1])    # Similarity
			results.append(row)
		except IndexError:
			row.append("sampleBlog") # Website
			row.append('#ec5868') # Back_Color
			row.append("#444444") # Link_Color
			row.append("#444444") # Text_Color
			row.append("Helvetica Neue") # Title_Font
			row.append("Helvetica Neue") # Body_Font
			row.append("sampleText") # Text
			row.append("0.0")    # Similarity
			results.append(row)
			break

	resultsDF = pd.DataFrame(results)

	resultsDF.columns = ['Website','BackColor','LinkColor','TextColor','TitleFont','BodyFont','Text','Similarity']
	resultsDF['Text'] = resultsDF['Text'].apply(regex_text)
	resultsDF = resultsDF.sort_values(by=['Similarity'],ascending=False)
	return resultsDF

def generateResultWeb(description):
	df = similarityWeb(description)
	dict = {}
	flag_f = False
	# aF = [ast.literal_eval(df.iloc[0]['Fonts']), ast.literal_eval(df.iloc[1]['Fonts']), ast.literal_eval(df.iloc[2]['Fonts'])]
	# aC = [ast.literal_eval(df.iloc[0]['Colours']), ast.literal_eval(df.iloc[1]['Colours']), ast.literal_eval(df.iloc[2]['Colours'])]
	# aT = [df.iloc[0]['Text'], df.iloc[1]['Text'], df.iloc[2]['Text']]
	try:
		aF = [ast.literal_eval(df.iloc[0]['Fonts']), ast.literal_eval(df.iloc[1]['Fonts']), ast.literal_eval(df.iloc[2]['Fonts'])]
		aC = [ast.literal_eval(df.iloc[0]['Colours']), ast.literal_eval(df.iloc[1]['Colours']), ast.literal_eval(df.iloc[2]['Colours'])]
		aT = [df.iloc[0]['Text'], df.iloc[1]['Text'], df.iloc[2]['Text']]
	except:
		aF = [df.iloc[0]['Fonts']]
		aC = [df.iloc[0]['Colours']]
		aT = [df.iloc[0]['Text']] 
		flag_f = True

	font_size = []
	for i in range(len(aF)):
		font_size.append(len(aF[i]))
		for j in range(len(aF[i])):
			aF[i][j][1] = int(aF[i][j][1])

	color_size = []
	for i in range(len(aC)):
		color_size.append(len(aC[i]))
		for j in range(len(aC[i])):
			if (' ' in aC[i][j][0]) or (',' in aC[i][j][0]):
				aC[i][j][0] = aC[i][j][0].replace(' ','')
				aC[i][j][0] = aC[i][j][0].replace(',','')

	if flag_f:
		font_size = [0]
		color_size = [0]

	dict['total'] = range(len(aC))
	dict['f_size'] = font_size
	dict['c_size'] = color_size
	dict['fonts'] = aF
	dict['colors'] = aC
	dict['texts'] = aT
	return dict

def generateResultBlog(description):
	df = similarityBlog(description)
	dict = {}
	try:
		aBC = [df.iloc[0]['BackColor'], df.iloc[1]['BackColor'], df.iloc[2]['BackColor'], df.iloc[3]['BackColor']]
		aLC = [df.iloc[0]['LinkColor'], df.iloc[1]['LinkColor'], df.iloc[2]['LinkColor'], df.iloc[3]['LinkColor']]
		aTC = [df.iloc[0]['TextColor'], df.iloc[1]['TextColor'], df.iloc[2]['TextColor'], df.iloc[3]['TextColor']]
		aTF = [df.iloc[0]['TitleFont'], df.iloc[1]['TitleFont'], df.iloc[2]['TitleFont'], df.iloc[3]['TitleFont']]
		aBF = [df.iloc[0]['BodyFont'], df.iloc[1]['BodyFont'], df.iloc[2]['BodyFont'], df.iloc[3]['BodyFont']]
	except:
		aBC = [df.iloc[0]['BackColor']]
		aLC = [df.iloc[0]['LinkColor']]
		aTC = [df.iloc[0]['TextColor']]
		aTF = [df.iloc[0]['TitleFont']]
		aBF = [df.iloc[0]['BodyFont']]

	dict['total'] = len(aBC)
	dict['back_color'] = aBC
	dict['link_color'] = aLC
	dict['text_color'] = aTC
	dict['title_font'] = aTF
	dict['body_font'] = aBF
	return dict


def get_blog_result(content):

	# load cached blog_model
	# transformed = blog_model.transform(content)

	# get dict of lists of top 3 recommending styles for each attribute
	# below is a sample result variable that I will use to build flask application

	result = generateResultBlog(content)

	# result = {'back_color': ['#FAFAFA', '#ec5868', '#847d81', '#FAFAFA'],
 # 'link_color': ['#529ECC', '#fce7aa', '#03131d', '#529ECC'],
 # 'text_color': ['#444444', '#fce7aa', '#444444', '#444444'],
 # 'title_font': ['Gibson', 'SimHei', 'Georgia', 'Gibson'],
 # 'body_font': ['Helvetica Neue',
 #  'Helvetica Neue',
 #  'Helvetica Neue',
 #  'Helvetica Neue']}

	return result


def get_web_result(content):

	# load cached web_model
	# transformed = web_model.transform(content)

	# get dict of lists of top 3 recommending styles for each attribute
	# below is a sample result variable that I will use to build flask application

	# result = {'f_size': [3, 3, 3],
 # 'c_size': [3, 3, 3],
 # 'fonts': [[["font-family:'fl-icons'", 4],
 #   ["font-family:'object-fit: cover", 3],
 #   ['font-family:"fl-icons" !important', 2]],
 #  [['font-family:Arial', 9],
 #   ['font-family: "revicons"', 8],
 #   ['font-family: FontAwesome', 5]],
 #  [['font-family:"Barlow Condensed",arial', 9],
 #   ['font-family:"Lato",arial', 7],
 #   ['font-family:arial', 4]]],
 # 'colors': [[['#446084', 15], ['#f1f1f1', 6], ['#d26e4b', 2]],
 #  [['#337ab7', 7], ['#f5f5f5', 6], ['#1980B6', 6]],
 #  [['#f9f9f9', 2], ['#5B5B5', 1], ['#e6e6e6', 1]]],
 # 'texts': ['...strain current Hot new Account banner Sale right last well taken saying col column submit level wholesale made best strong produce Tour gallery every image little season are few before when dysfunction wondering transparent living place our used Contact receive should Cart favored intercourse Border slider mushroom syringes very visible....',
 #  '...modal fight VIDEO Story Video image Add pull plus share this LECTURE white Remember target blank role radius suggest body from Mobile account You Menu was twitter ref font one their document display them Interesting have interest SIGN AND History Science inventor but Coil Assembly password world SEARCH could about Short Sign switch....',
 #  '...The fair THE Volleyball Cite Baseball personal DEADLINE rum footer LOGOS GOLF Athletic body sports LEADERSHIP responsibility Skip ATHLETE Softball Home for educational Search GENERAL practice Twitter offering athletic inBeing forum process Composite academic Leadership theme active BASEBALL....']}

	result = generateResultWeb(content)

	return result

