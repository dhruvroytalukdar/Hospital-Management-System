from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '89461sdf6ds554f6546546ds54fs646546'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
db = SQLAlchemy(app)

from HMS import routes