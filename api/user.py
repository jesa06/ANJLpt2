import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from model.users import User, Weather
from __init__ import db, app

user_api = Blueprint('user_api', __name__,
                     url_prefix='/api/users')

api = Api(user_api)

class UserAPI:
    def __init__(self):
        pass

    class _CR(Resource):
        def post(self): # create method
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
            
            user = uo.create() # adds to sqlite
            if user:
                return jsonify(user.read())
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps



    class _Login(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400

            
            ''' Find user '''
            #user = user.find_by_uid(uid)
            #if user and user.check_credentials(uid, password):
             #   return jsonify(user.read())
            #else:
             #   return {'message': f"Invalid user id or password"}, 400
            user = User.query.filter_by(_uid=uid).first()
            #if user is not None and user.is_password(password):
            if user and user.find_by_uid(uid):
                return jsonify(user.read())
            else:
                return {'message': f"User does not exist"}, 400
        


    class _Weather(Resource):
        def post(self):
            body = request.get_json()

            uid = body.get('uid')
            city = body.get('city')
            dos = body.get('dos')

            user = User.query.filter_by(uid=uid).first()

            if not user:
                return {'message': 'User not found.'}, 404

            wo = User(uid=uid,
                      city=city,
                      dos=dos)
            
            if dos is not None:
                try:
                    wo.dos = datetime.strptime(dos, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of search format error {dos}, must be yyyy-mm-dd'}, 400
            
            weather = wo.create() # adds to sqlite
            if weather:
                return jsonify(weather.read())
            return {'message': f'Processed {city}, either a format error'}, 400
        

           



    # building RESTapi endpoint
    api.add_resource(_CR, '/')
    api.add_resource(_Login, '/login')
    api.add_resource(_Weather, '/saveWeather')