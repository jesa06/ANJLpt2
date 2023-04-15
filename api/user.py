import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from model.users import User
from __init__ import db, app

user_api = Blueprint('user_api', __name__,
                     url_prefix='/api/users')

api = Api(user_api)

class UserAPI:
    def __init__(self):
        pass

        
    class _Create(Resource):
        def post(self):
            body = request.get_json()
            
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            
            password = body.get('password')
            dob = body.get('dob')
            phone = body.get('phone')
            email = body.get('email')
            age = body.get('age')
            
            uo = User(name=name, 
                      uid=uid,
                      phone=phone,
                      email=email,
                      password=password,
                      dob=dob,
                      age=age)
            
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be yyyy-mm-dd'}, 400
            
            user = uo.create()
            if user:
                return jsonify(user.read())
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            users = User.query.all()
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)
    

    class _Login(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')

            
            ''' Find user '''
            user = User.query.filter_by(_uid=uid).first()
            if user is None or not user.is_password(password):
            #if user is None or not user.check_credentials(uid, password):
                return {'message': f"Invalid user id or password"}, 400
            

            ''' authenticated user ''' 
            return jsonify(user.read())

        

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Login, '/authenticate')
    