#!/usr/bin/env python3
from random import choice as rc
from faker import Faker
from app import app
from models import *
import datetime

# db.init_app(app)
fake = Faker()
with app.app_context():
    User.query.delete()
    users= []
    for n in range(50):
        user = User(name=fake.name(),email=fake.email(), _password_hash=fake.password())
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
