
def get_blog_result(content):

	# load cached blog_model
	# transformed = blog_model.transform(content)

	# get dict of lists of top 3 recommending styles for each attribute
	# below is a sample result variable that I will use to build flask application

	result = {
		'title_font': ['Courier New','Gibson','Times','Courier New'],
		'body_font': ['Times','Courier New','Helvetica Neue','Courier New'],
		'back_color': ['#c389cc','#d4e8ff','#5ee682','#c389cc'],
		'text_color': ['#7a5835','#8a8563','#444444','#7a5835'],
		'link_color': ['#2c451d','#529ECC','#9767a1','#9767a1']
	}

	return result


def get_web_result(content):

	# load cached web_model
	# transformed = web_model.transform(content)

	# get dict of lists of top 3 recommending styles for each attribute
	# below is a sample result variable that I will use to build flask application

	result = {'f_size': [3, 3, 3],
 		'c_size': [3, 3, 3],
		'colors': [[['#f9f9f9', 2], ['#141a64', 1], ['#e6e6e6', 1]],
				 [['#f9f9f9', 2], [' #5B5B5', 1], ['#e6e6e6', 1]],
				 [['#404040', 1], ['#F06D65', 1], ['#f1f1f1', 1]]],
		'fonts': [[["font-family: 'raleway'", 6], ['font-family:arial', 5], ['font-family:"GlyphIcons"', 3]],
				 [['font-family:"Barlow Condensed",arial', 9], ['font-family:"Lato",arial', 7], ['font-family:arial', 4]],
				 [["font-family: 'Roboto', sans-serif", 9], ['font-family: Arial, Helvetica, sans-serif', 1], ["font-family:'FontAwesome'", 1]]],
		'texts': ['......Model Root Testing system aSkip inside fingerprinting Group climate tool molecular Liquid the sample any for Room lab growth Research Cabinet vision biological Saving environment TESTING advanced cooling heating Growth classification computer Search analytics SCIENCE distributed test.......',
  '......Hill with transparent more child media Permanent Ping browse Fall document social FREE all green Holiday Shuffleboard The Day radius Virtual PARTY bowl video Eve bookmark Here Contact Field you alpha available virtual premiere Home SLIDER world Happening Memory Gallery drawn Click Corporate Skeleton Big Event Roller for subject below.......',
  '......based been creator Code Available much code love really Copilot into search ready IDE all give within use one great myself Mac today Atom ranked through was documentation Being Holy try seamless many Kyle plethora you function its NEW Faster applied kite this just and Save cog Bret for past.......']
	}

	return result

