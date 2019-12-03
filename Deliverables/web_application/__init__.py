from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xd8\xa3\xb5c\xf2\x0c\x93\xcc#\x94\x17n\xbdhv\xc5~0\xa8\xd6+\xfd\xcf\xd1'

from web_application import templates