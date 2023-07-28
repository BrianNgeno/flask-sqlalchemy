from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

class User(db.Model,SerializerMixin):
    __tablename__='users'
    
    serialize_rules =('-car.user')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String,unique=True,nullable=True)
    _password_hash = db.Column(db.String,nullable=False)
    car  = db.relationship('Car',backref='user')




    def __repr__(self):
        return f'user {self.name} has been created'


    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    # @password.setter
    # def password_hash(self, password):
    #     self._password_hash=self.simple_hash(password)

    def authenticate(self, password):
        return self.simple_hash(password)== self.password_hash
    
    @staticmethod
    def simple_hash(input):
        return sum(bytearray(input, encoding='utf-8'))

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email
        }

    @validates('email')
    def validate_email(self,key,users):
        if '@' not in users:
            ValueError("enter a valid email")
        else:
            return users
 

class Car(db.Model,SerializerMixin):
    ___tablename__ = 'cars'
    serialize_rules =('-user.car')

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return f'car {self.make} has been created'


