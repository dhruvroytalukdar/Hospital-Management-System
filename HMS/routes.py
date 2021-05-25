from HMS.models import *
from flask import render_template
from HMS import app


@app.route('/')
def home():
    return render_template('home.html', name="Dhruv Roy Talukdar")
