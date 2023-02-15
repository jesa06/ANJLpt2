from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

activity_api = Blueprint('activity_api', __name__,
                   url_prefix='/api/activities')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(activity_api)

class ActivityApi:        
    class _Create(Resource):
        def post(activity):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate hobby
            hobby = body.get('hobby')
            # validate price
            price = body.get('price')
            # validate duration
            duration = body.get('duration')
            

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Activity(activity=name)
            
            ''' Additional garbage error checking '''
            uo.hobby = hobby
            # set password if provided
            uo.price = price
            # convert to date type
            uo.duration = duration
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or Activity {name} is duplicate'}, 210

    class _Read(Resource):
        def get(activity):
            activities = activity.query.all()    # read/extract all users from database
            json_ready = [activity_api.read() for activity in activities]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')