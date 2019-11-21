from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from web_application import app
from web_application.generate_result import gen_result
from web_application.popular_result import pop_result, pop_topics
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

web_name = 'Web Crawl Style Creator'
# we may or may not use the below feature
popular_topics = pop_topics()


class PostForm(FlaskForm):
	content = TextAreaField('Content', validators=[DataRequired()])
	# url = StringField('url', validators=[DataRequired()])
	submit = SubmitField('OK')


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', name=web_name, popular=popular_topics)

@app.route('/website', methods=['GET', 'POST'])
def website():
	form = PostForm()
	if form.validate_on_submit():
		returned = gen_result('web', form.content.data)
		title_font = returned['title_font']
		body_font = returned['body_font']
		back_color = returned['back_color']
		text_color = returned['text_color']
		link_color = returned['link_color']
		return render_template('result.html', name=web_name, \
			title_font=title_font, body_font=body_font, \
			back_color=back_color, text_color=text_color, link_color=link_color, \
			popular=popular_topics)
	return render_template('website.html', name=web_name, form=form, popular=popular_topics)

@app.route('/blog', methods=['GET', 'POST'])
def blog():
	form = PostForm()
	if form.validate_on_submit():
		returned = gen_result('blog', form.content.data)
		title_font = returned['title_font']
		body_font = returned['body_font']
		back_color = returned['back_color']
		text_color = returned['text_color']
		link_color = returned['link_color']
		return render_template('result.html', name=web_name, \
			title_font=title_font, body_font=body_font, \
			back_color=back_color, text_color=text_color, link_color=link_color, \
			popular=popular_topics)
	return render_template('blog.html', name=web_name, form=form, popular=popular_topics)

@app.route('/about')
def about():
	return render_template('about.html', title='About', name=web_name, popular=popular_topics)

@app.route('/result')
def result():
	topic = request.args['topic']
	if len(topic) > 0:
		returned = pop_result(topic)
		title_font = returned['title_font']
		body_font = returned['body_font']
		back_color = returned['back_color']
		text_color = returned['text_color']
		link_color = returned['link_color']
	return render_template('result.html', name=web_name, \
		title_font=title_font, body_font=body_font, \
		back_color=back_color, text_color=text_color, link_color=link_color, \
		popular=popular_topics)

if __name__ == '__main__':
	app.run(debug=True)


