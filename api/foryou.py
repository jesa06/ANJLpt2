from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource  # used for REST API building
from sqlalchemy.exc import IntegrityError

from models import Activity, db

activity_api = Blueprint('activity_api', __name__, url_prefix='/api/activities')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(activity_api)


class ActivityApi:
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()

            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate hobby
            hobby = body.get('hobby')
            # validate price
            price = body.get('price')
            # validate duration
            duration = body.get('duration')

            ''' #1: Key code block, setup ACTIVITY OBJECT '''
            ao = Activity(name=name)

            ''' Additional garbage error checking '''
            ao.hobby = hobby
            ao.price = price
            ao.duration = duration
            ao.location = location

            ''' #2: Key Code block to add user to database '''
            # create user in database
            db.session.add(ao)
            try:
                db.session.commit()
                return jsonify(ao.to_dict()), 201  # success returns json of activity
            except IntegrityError:
                db.session.rollback()
                return {'message': f'Activity {name} already exists'}, 409

    class _Read(Resource):
        def get(self):
            activities = Activity.query.all()  # read/extract all users from database
            json_ready = [activity.to_dict() for activity in activities]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')