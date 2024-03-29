from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '89461sdf6ds554f6546546ds54fs646546'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hms.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from HMS import routes