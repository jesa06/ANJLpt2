import json
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.seaworld import Seaworld

seaworld_api = Blueprint('seaworld_api', __name__,
                   url_prefix='/api/seaworld')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(seaworld_api)

class SeaworldAPI:        
    class _Create(Resource):
        def put(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            rating = body.get('rating')
            review = body.get('review')
            recommend = body.get('recommend')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Seaworld(name=name, 
                      uid=uid)
            uo.rating = rating
            uo.review = review
            uo.recommend = recommend

            ''' Additional garbage error checking '''
            # set password if provided
          #   if password is not None:
             #   uo.password = password
    
            # convert to date type
        
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            seaworld = uo.create()
            # success returns json of user
            if seaworld:
                return jsonify(seaworld.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

    class _Read(Resource):
        def get(self):
            seaworld = Seaworld.query.all()    # read/extract all users from database
            json_ready = [seaworld.read() for seaworld in seaworld]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Security(Resource):

        def put(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Get Data '''
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            password = body.get('password')

            
            ''' Find user '''
            seaworld = Seaworld.query.filter_by(_uid=uid).first()
            if seaworld is None or not seaworld.is_password(password):
                return {'message': f"Invalid user id or password"}, 400
            
            ''' authenticated user ''' 
            return jsonify(seaworld.read())

            

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_Security, '/authenticate')
    