from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from web_application_2 import app
from web_application_2.generate_result import get_blog_result, get_web_result
from web_application_2.popular_result import pop_result_blog, pop_result_web, pop_topics_blog, pop_topics_web
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


web_name = 'Web Crawl Style Creator'
# we may or may not use the below feature
pop_topics_blog = pop_topics_blog()
pop_topics_web = pop_topics_web()


class PostForm(FlaskForm):
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('OK')


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', name=web_name)
		# popular_web=pop_topics_web, popular_blog=pop_topics_blog)

@app.route('/website', methods=['GET', 'POST'])
def website():
	form = PostForm()
	if form.validate_on_submit():
		returned = get_web_result(form.content.data)
		colors = returned['colors']
		fonts = returned['fonts']
		f_size = returned['f_size']
		c_size = returned['c_size']
		total = returned['total']
		texts = form.content.data
		return render_template('result_web.html', name=web_name, \
			colors=colors, fonts=fonts, texts=texts, f_size=f_size, c_size=c_size, total=total)
			# popular_web=pop_topics_web, popular_blog=pop_topics_blog)
	return render_template('website.html', name=web_name, form=form)
		# popular_web=pop_topics_web, popular_blog=pop_topics_blog)

@app.route('/result_web')
def result_web():
	# topic = request.args['topic']
	# if len(topic) > 0:
	# 	returned = pop_result_web(topic)
	# 	colors = returned['colors']
	# 	fonts = returned['fonts']
	# 	texts = returned['texts']
	# 	f_size = returned['f_size']
	# 	c_size = returned['c_size']
	return render_template('result_web.html', name=web_name, \
		colors=colors, fonts=fonts, texts=texts, f_size=f_size, c_size=c_size, total=total)
		# popular_web=pop_topics_web, popular_blog=pop_topics_blog, topic=topic)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
	form = PostForm()
	if form.validate_on_submit():
		returned = get_blog_result(form.content.data)
		title_font = returned['title_font']
		body_font = returned['body_font']
		back_color = returned['back_color']
		text_color = returned['text_color']
		link_color = returned['link_color']
		total = returned['total']
		raw_text = form.content.data
		texts = raw_text
		if len(texts) > 33:
			texts = texts[:33] + "...."

		return render_template('result_blog.html', name=web_name, \
			title_font=title_font, body_font=body_font, \
			back_color=back_color, text_color=text_color, link_color=link_color, \
			texts=texts, raw_text=raw_text, total=total)
			# texts=texts, raw_text=raw_text, popular_web=pop_topics_web, popular_blog=pop_topics_blog)
	return render_template('blog.html', name=web_name, form=form) 
		# popular_web=pop_topics_web, popular_blog=pop_topics_blog)

@app.route('/result_blog')
def result_blog():
	# topic = request.args['topic']
	# if len(topic) > 0:
	# 	returned = pop_result_blog(topic)
	# 	title_font = returned['title_font']
	# 	body_font = returned['body_font']
	# 	back_color = returned['back_color']
	# 	text_color = returned['text_color']
	# 	link_color = returned['link_color']
	return render_template('result_blog.html', name=web_name, \
		title_font=title_font, body_font=body_font, \
		back_color=back_color, text_color=text_color, link_color=link_color, \
		texts=texts, raw_text=raw_text, total=total)
		# texts=texts, raw_text=raw_text, popular_web=pop_topics_web, popular_blog=pop_topics_blog, topic=topic)

@app.route('/link_blog')
def link_blog():
	ititle_font = request.args['ititle_font']
	ibody_font = request.args['ibody_font']
	iback_color = request.args['iback_color']
	itext_color = request.args['itext_color']
	ilink_color = request.args['ilink_color']
	raw_text = request.args['raw_text']
	texts = request.args['texts']
	return render_template('link_blog.html', name=web_name, \
		raw_text=raw_text, ititle_font=ititle_font, ibody_font=ibody_font, \
		iback_color=iback_color, itext_color=itext_color, ilink_color=ilink_color,)

@app.route('/about')
def about():
	return render_template('about.html', title='About', name=web_name)
		# popular_web=pop_topics_web, popular_blog=pop_topics_blog)

if __name__ == '__main__':
	app.run(debug=True)


