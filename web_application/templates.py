from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from web_application import app
from web_application.generate_result import get_blog_result, get_web_result
from web_application.popular_result import pop_result_blog, pop_result_web, pop_topics_blog, pop_topics_web
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

web_name = 'Web Crawl Style Creator'
# we may or may not use the below feature
pop_topics_blog = pop_topics_blog()
pop_topics_web = pop_topics_web()


class PostForm(FlaskForm):
	content = TextAreaField('Content', validators=[DataRequired()])
	# url = StringField('url', validators=[DataRequired()])
	submit = SubmitField('OK')


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', name=web_name, popular=pop_topics_web)

@app.route('/website', methods=['GET', 'POST'])
def website():
	form = PostForm()
	if form.validate_on_submit():
		returned = get_web_result(form.content.data)
		colors = returned['colors']
		fonts = returned['fonts']
		return render_template('result_web.html', name=web_name, \
			colors=colors, fonts=fonts, popular=pop_topics_web)
	return render_template('website.html', name=web_name, form=form, popular=pop_topics_web)

@app.route('/result_web')
def result_web():
	topic = request.args['topic']
	if len(topic) > 0:
		returned = pop_result_web(topic)
		colors = returned['colors']
		fonts = returned['fonts']
	return render_template('result_web.html', name=web_name, \
		colors=colors, fonts=fonts, popular=pop_topics_web, topic=topic)

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
		return render_template('result_blog.html', name=web_name, \
			title_font=title_font, body_font=body_font, \
			back_color=back_color, text_color=text_color, link_color=link_color, \
			popular=pop_topics_blog)
	return render_template('blog.html', name=web_name, form=form, popular=pop_topics_blog)

@app.route('/result_blog')
def result_blog():
	topic = request.args['topic']
	if len(topic) > 0:
		returned = pop_result_blog(topic)
		title_font = returned['title_font']
		body_font = returned['body_font']
		back_color = returned['back_color']
		text_color = returned['text_color']
		link_color = returned['link_color']
	return render_template('result_blog.html', name=web_name, \
		title_font=title_font, body_font=body_font, \
		back_color=back_color, text_color=text_color, link_color=link_color, \
		popular=pop_topics_blog, topic=topic)

@app.route('/about')
def about():
	return render_template('about.html', title='About', name=web_name, popular=pop_topics_web)

if __name__ == '__main__':
	app.run(debug=True)


