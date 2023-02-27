from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from model.activity import Activity

activity_api = Blueprint('activity_api', __name__, url_prefix='/api/activities')
api = Api(activity_api)

class ActivityApi:
    class _Create(Resource):
        def post(self):
            ''' Read data from json body '''
            body = request.get_json()

            ''' Error checking '''
            # validate name
            name = body.get('name')
            if not name or len(name) < 2:
                return {'message': 'Activity name is missing, or is less than 2 characters'}, 400

            # validate hobby
            hobby = body.get('hobby')
            
            # validate price
            price = body.get('price')

            # validate duration
            duration = body.get('duration')
            
            # validate location
            location = body.get('location')

            ''' Key code block, setup ACTIVITY OBJECT '''
            ao = Activity(name=name, hobby=hobby, price=price, duration=duration, location=location)

    class _Read(Resource):
        def get(self):
            activities = Activity.query.all()
            json_ready = [activity.to_dict() for activity in activities]
            return jsonify(json_ready)
        
    class _Security(Resource):

        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Find activity '''
            activity = Activity.query.filter_by().first()
            if activity is None:
                return {'message': f"Invalid activity"}, 400
            
            ''' authenticated user ''' 
            return jsonify(activity.read())

    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
