
def gen_result(post_type, content):

	if post_type == "blog":
		# load cached blog_model
		# transformed = blog_model.transform(content)
		t = ""
	elif post_type == "web":
		# load cached web_model
		# transformed = web_model.transform(content)
		t = ""
	else:
		# transformed = None
		t = ""

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

