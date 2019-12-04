# we will do it if we have extra time 


def pop_topics_blog():

	# create a list of top 5 popular topics 
	# (To shorten the running time, we may insert the topics into the cassandra table in other code and just select here)
	# below is a sample result variable that I will use to build flask application

	result = ['blog1', 'anime', 'shopping']

	return result

def pop_topics_web():

	# create a list of top 5 popular topics 
	# (To shorten the running time, we may insert the topics into the cassandra table in other code and just select here)
	# below is a sample result variable that I will use to build flask application

	result = ['web1', 'web2', 'web topic 3']

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

	# result = {'f_size': [3, 3, 3],
	#	 'c_size': [3, 3, 3],
	# 	'colors': [[['#f9f9f9', 2], ['#141a64', 1], ['#e6e6e6', 1]],
	# 			 [['#f9f9f9', 2], [' #5B5B5', 1], ['#e6e6e6', 1]],
	# 			 [['#404040', 1], ['#F06D65', 1], ['#f1f1f1', 1]]],
	# 	'fonts': [[["font-family: 'raleway'", 6], ['font-family:arial', 5], ['font-family:"GlyphIcons"', 3]],
	# 			 [['font-family:"Barlow Condensed",arial', 9], ['font-family:"Lato",arial', 7], ['font-family:arial', 4]],
	# 			 [["font-family: 'Roboto', sans-serif", 9], ['font-family: Arial, Helvetica, sans-serif', 1], ["font-family:'FontAwesome'", 1]]],
	# 	'texts': ['......Model Root Testing system aSkip inside fingerprinting Group climate tool molecular Liquid the sample any for Room lab growth Research Cabinet vision biological Saving environment TESTING advanced cooling heating Growth classification computer Search analytics SCIENCE distributed test.......',
 #  '......Hill with transparent more child media Permanent Ping browse Fall document social FREE all green Holiday Shuffleboard The Day radius Virtual PARTY bowl video Eve bookmark Here Contact Field you alpha available virtual premiere Home SLIDER world Happening Memory Gallery drawn Click Corporate Skeleton Big Event Roller for subject below.......',
 #  '......based been creator Code Available much code love really Copilot into search ready IDE all give within use one great myself Mac today Atom ranked through was documentation Being Holy try seamless many Kyle plethora you function its NEW Faster applied kite this just and Save cog Bret for past.......']
	# }

	# result of running "big data and machine learning"
	result = {'f_size': [3, 3, 3],
		 'c_size': [3, 3, 3],
		 'fonts': [[['font-family:icomoo', 7],
		   ['font-family:IcoMoon', 7],
		   ['font-family:DaxCondensedLight, Arial, Helvetica, sans-serif', 7]],
		  [['font-family:"Lucida Grande","Lucida Sans Unicode",Tahoma,sans-serif', 8],
		   ['font-family:"Lucida Grande","Lucida Sans Unicode",Tahoma,sans-serif !important',
		    7],
		   ["font-family: 'FontAwesome'", 2]],
		  [['font-family:Neue Frutiger W01,sans-serif', 8],
		   ['font-family:Droid Sans Mono W01,monospace', 7],
		   ['font-family:"Neue Frutiger W01"', 6]]],
		 'colors': [[['#ffffff', 22], ['#a0ce4e', 12], ['#f6f6f6', 9]],
		  [['#ffffff', 13], ['#ffffff', 7], ['#008ec', 7]],
		  [['#14b4c3', 15], ['#24273f', 12], ['#11182f', 11]]],
		 'texts': ['...Model Root Testing system aSkip inside fingerprinting Group climate tool molecular Liquid the sample any for Room lab growth Research Cabinet vision biological Saving environment TESTING advanced cooling heating Growth classification computer Search analytics SCIENCE distributed test....',
		  '...Hill with transparent more child media Permanent Ping browse Fall document social FREE all green Holiday Shuffleboard The Day radius Virtual PARTY bowl video Eve bookmark Here Contact Field you alpha available virtual premiere Home SLIDER world Happening Memory Gallery drawn Click Corporate Skeleton Big Event Roller for subject below....',
		  '...based been creator Code Available much code love really Copilot into search ready IDE all give within use one great myself Mac today Atom ranked through was documentation Being Holy try seamless many Kyle plethora you function its NEW Faster applied kite this just and Save cog Bret for past....']
		}

	return result