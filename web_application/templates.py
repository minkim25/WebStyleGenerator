from flask import Flask, render_template, url_for
app = Flask(__name__)

web_name = 'Web Crawl Style Creator'

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', name=web_name)

@app.route('/about')
def about():
	return render_template('about.html', title='About', name=web_name)

@app.route('/result')
def result():
	return render_template('result.html', name=web_name)

if __name__ == '__main__':
	app.run(debug=True)


