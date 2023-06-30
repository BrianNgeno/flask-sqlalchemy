#!/usr/bin/env python3
import os
from flask import Flask, jsonify, make_response,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException, NotFound
from models import db,User
from flask_cors import CORS





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# app.config['JSONIFY_PRETTYPRINT_REGULAR']=True
app.secret_key= b'm{\xf9\xec\xa0\xa7Gv\x98\x07\xa9\xfb\xdb\xe2\x8d\x86'

app.json.compact =  False
CORS(app)

migrate = Migrate(app, db)

api = Api(app)

db.init_app(app)



class Index(Resource):
    def get(self):
        response_dict = {
            "index":"Welcome user"
        }
        response= make_response(
            jsonify(response_dict),
            200
        )

        return response
    
    
api.add_resource(Index,'/')

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

api.add_resource(ClearSession, '/clear')

class Users(Resource):
    def get(self):
        
        user_dictionary= [x.to_dict() for x in User.query.all()]
        response = make_response(
            jsonify(user_dictionary),
            200,
        )
        return response
    
    def post(self):
        data = User(
            email = request.get_json()['email'],
            name = request.get_json()['name']
        )
        db.session.add(data)
        db.session.commit()
        data_dict = data.to_dict()
        response = make_response(
            jsonify(data_dict),
            201,
        )
        return response

api.add_resource(Users,'/users')


class UserByID(Resource):

    def patch(self,id):
        record = User.query.filter_by(id=id).first()
        for data in request.form:
            data(record, data,request.form[data])
        db.session.delete(record)
        db.session.commit()
        response_dict = record.to_dict()
        response = make_response(
            jsonify(response_dict),
            200
        )
        return response

    def delete(self,id):
        
        record = User.query.filter_by(id=id).first()
        db.session.delete(record)
        db.session.commit()
        response_dict={
            "message":"user deleted successfully"
        }
        response = make_response(
            jsonify(response_dict)
        )
    
        return response 

    def put(self,id):
        return

api.add_resource(UserByID,'/users/<int:id>')


class Login(Resource):

    def post(self):
        
        email = request.get_json()['email']
        
        user = User.query.filter(User.email == email ).first()

        password = request.get_json()['password']
        if password == user.password:
            session['user_id'] = user.id
            return user.to_dict(), 200
        else:
            return {'message':"invalid username or password"}

class Logout(Resource):
    def get(self):
        session['user_id']= None 
        return jsonify({'messsage':'successfully logged out'}) 

api.add_resource(Logout,'/logout')      

api.add_resource(Login, '/login')

@app.errorhandler(NotFound)
def handle_notfound(e):
    response=make_response(
        "Not found:system under maintance check back later",
        404
    )
    return response

@app.errorhandler(HTTPException)
def handle_server_error(e):
    response=make_response(
        "Server Error:system server under maintance check back later",
        500
    )
    return response

class showSession(Resource):
    def get(self, key):
        session["home"] = session.get("home")

        response = make_response(jsonify({
            "session":{
                'session_key':key,
                'session_value':session[key],
                'session_accessible':session.accessed,
            },
            'cookies':[{cookie: request.cookies[cookie]}
                for cookie in request.cookies],
                }),200
        )
        response.set_cookie('mouse','Cookie')
        return response
api.add_resource(showSession,'/sessions/<string:key>')


class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id== session.get('user_id')).first()
        if user:
            print(user)
            return user.to_dict()
        else:
            return jsonify({"message":'401:Not authorized'}), 401

api.add_resource(CheckSession,'/checksession')


if __name__ == '__main__':
    app.run(port=5000)