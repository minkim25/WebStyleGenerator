from flask import Flask, render_template, url_for

app = Flask(__name__)
web_name = 'Web Crawl Style Creator'

# sample returned results 
title_font = ['Gibson','Gibson','Gibson']
body_font  = ['Times','Courier New','Helvetica Neue']
back_color = ['#5ee682','#d4e8ff','#c389cc']
text_color = ['#7a5835','#8a8563','#444444']
link_color = ['#2c451d','#529ECC','#9767a1']

popular_topics = ['popular topic 1', 'popular topic 2', 'popular topic 3', 'popular topic 4', 'popular topic 5']


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', name=web_name, popular=popular_topics)

@app.route('/website')
def website():
	return render_template('website.html', name=web_name, popular=popular_topics)

@app.route('/blog')
def blog():
	return render_template('blog.html', name=web_name, popular=popular_topics)

@app.route('/about')
def about():
	return render_template('about.html', title='About', name=web_name, popular=popular_topics)

@app.route('/result')
def result():
	return render_template('result.html', name=web_name, \
		title_font=title_font, body_font=body_font, \
		back_color=back_color, text_color=text_color, link_color=link_color, \
		popular=popular_topics)

if __name__ == '__main__':
	app.run(debug=True)


