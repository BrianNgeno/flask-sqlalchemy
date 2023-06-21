#!/usr/bin/env python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///my_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    # topic = '<h1>Hello world!</h1>'
    return '<h1>Hello world!</h1>'

@app.route('/<string:name>')
def members(name):
    return f'<h2>Welcome user {name}</h2>'

if __name__ == '__main__':
    app.run(port=5000)