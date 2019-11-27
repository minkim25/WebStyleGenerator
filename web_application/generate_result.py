
def get_blog_result(content):

	# load cached web_model
	# transformed = web_model.transform(content)

	# get dict of lists of top 3 recommending styles for each attribute
	# below is a sample result variable that I will use to build flask application

	result = {
		'title_font': ['Courier New','Gibson','Times'],
		'body_font': ['Times','Courier New','Helvetica Neue'],
		'back_color': ['#5ee682','#d4e8ff','#c389cc'],
		'text_color': ['#7a5835','#8a8563','#444444'],
		'link_color': ['#2c451d','#529ECC','#9767a1']
	}

	return result


def get_web_result(content):

	# load cached blog_model
	# transformed = blog_model.transform(content)

	# get dict of lists of top 3 recommending styles for each attribute
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

