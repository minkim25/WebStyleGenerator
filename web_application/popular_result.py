# we will do it if we have extra time 


def pop_topics_blog():

	# create a list of top 5 popular topics 
	# (To shorten the running time, we may insert the topics into the cassandra table in other code and just select here)
	# below is a sample result variable that I will use to build flask application

	result = ['blog1', 'anime', 'shopping', 'popular topic 4', 'popular topic 5']

	return result

def pop_topics_web():

	# create a list of top 5 popular topics 
	# (To shorten the running time, we may insert the topics into the cassandra table in other code and just select here)
	# below is a sample result variable that I will use to build flask application

	result = ['web1', 'web2', 'web3', 'popular topic 4', 'popular topic 5']

	return result


def pop_result_blog(topic):

	# parameter = selected topic from side-bar option
	# return dict of lists of top 3 recommending styles for each attribute
	# below is a sample result variable that I will use to build flask application

	result = {
		'title_font': ['Courier New','Gibson','Times','Courier New'],
		'body_font': ['Times','Courier New','Helvetica Neue','Courier New'],
		'back_color': ['#c389cc','#d4e8ff','#5ee682','#c389cc'],
		'text_color': ['#7a5835','#8a8563','#444444','#7a5835'],
		'link_color': ['#2c451d','#529ECC','#9767a1','#9767a1']
	}

	return result

def pop_result_web(topic):

	# parameter = selected topic from side-bar option
	# return dict of lists of top 3 recommending styles for each attribute
	# below is a sample result variable that I will use to build flask application

	result = {
		'colors': [[['#f9f9f9', 2], ['#141a64', 1], ['#e6e6e6', 1]],
				 [['#f9f9f9', 2], [' #5B5B5', 1], ['#e6e6e6', 1]],
				 [['#404040', 1], ['#F06D65', 1], ['#f1f1f1', 1]]],
		'fonts': [[["font-family: 'raleway'", 6], ['font-family:arial', 5], ['font-family:"GlyphIcons"', 3]],
				 [['font-family:"Barlow Condensed",arial', 9], ['font-family:"Lato",arial', 7], ['font-family:arial', 4]],
				 [["font-family: 'Roboto', sans-serif", 9], ['font-family: Arial, Helvetica, sans-serif', 1], ["font-family:'FontAwesome'", 1]]]
	}

	return result