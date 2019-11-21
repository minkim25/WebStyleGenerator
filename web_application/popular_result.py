# we will do it if we have extra time 


def pop_topics():

	# create a list of top 5 popular topics 
	# (To shorten the running time, we may insert the topics into the cassandra table in other code and just select here)
	# below is a sample result variable that I will use to build flask application

	result = ['sports', 'anime', 'shopping', 'popular topic 4', 'popular topic 5']

	return result


def pop_result(topic):

	# parameter = selected topic from side-bar option
	# return dict of lists of top 3 recommending styles for each attribute
	# below is a sample result variable that I will use to build flask application

	result = {
		'title_font': ['Courier New','Gibson','Times'],
		'body_font': ['Times','Courier New','Helvetica Neue'],
		'back_color': ['#c389cc','#d4e8ff','#5ee682'],
		'text_color': ['#7a5835','#8a8563','#444444'],
		'link_color': ['#2c451d','#529ECC','#9767a1']
	}

	return result