""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

#from flask import Blueprint, request, jsonify
#from flask_restful import Api, Resource # used for REST API building
#from datetime import datetime


# blueprint, which is registered to app in main.py
#user_api = Blueprint('user_api', __name__,
                   #url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html#id1
#api = Api(user_api)
#class UserAPI:        
    #class _Create(Resource):
        #def post(self):
            #''' Read data for json body '''
            #body = request.get_json()
            
            #''' Avoid garbage in, error checking '''
            # validate name
            #name = body.get('name')
            #if name is None or len(name) < 2:
                #return {'message': f'name is missing, or is less than 2 characters'}, 210
            # validate airline
            #airline = body.get('airline')
            #if airline is None or len(airline) < 2:
                #return {'message': f'airline is missing, or is less than 2 characters'}, 210
            # validate hotel
            #hotel = body.get('hotel')
            #if hotel is None or len(hotel) < 2:
                #return {'message': f'hotel is missing, or is less than 2 characters'}, 210
            # validate dob
            #duration = body.get('duration')
            #if duration is None or len(duration) < 2:
            #    return {'message': f'duration is missing, or is less than 2 characters'}, 210
            # look for password and dob
            #password = body.get('password')
            #dob = body.get('dob')

           # ''' #1: Key code block, setup USER OBJECT '''
           # uo = User(name=name, 
           #           airline=airline,
           #           hotel=hotel,
           #           duration=duration)
            
          #  ''' Additional garbage error checking '''
            # set password if provided
            #if password is not None:
                #uo.set_password(password)
            # convert to date type
            #if dob is not None:
                #try:
                    #uo.dob = datetime.strptime(dob, '%m-%d-%Y').date()
                #except:
                    #return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 210
            
            #''' #2: Key Code block to add user to database '''
            # create user in database
            #user = uo.create()
            # success returns json of user
            #if user:
               #return jsonify(user.read())
            # failure returns error
            #return {'message': f'Processed {name}, either a format error or User ID {airline} is duplicate'}, 210

    #class _Read(Resource):
       # def get(self):
       ##     users = User.query.all()    # read/extract all users from database
       #     json_ready = [user.read() for user in users]  # prepare output in json
        #    return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
 #   api.add_resource(_Create, '/create')
  #  api.add_resource(_Read, '/')

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Put(db.Model):
    __tablename__ = 'put'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('yelp.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Yelp(db.Model):
    __tablename__ = 'yelp'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _rating = db.Column(db.String(255), unique=False, nullable=False)
    _review = db.Column(db.String(255), unique=False, nullable=False)
    _activity = db.Column(db.Integer, unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    put = db.relationship("Put", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, rating, review="super good", activity='seaworld'):
        self._name = name    # variables with self prefix become part of the object, 
        self._rating = rating
        self._review = review
        self.activity = activity

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def rating(self):
        return self._rating
    
    # a setter function, allows name to be updated after initial object creation
    @rating.setter
    def rating(self, rating):
        self._rating = rating
        
    # check if airline parameter matches user id in object, return boolean
    def is_rating(self, rating):
        return self._rating == rating
    
    @property
    def review(self):
        return self._review[0:10] + "..." # because of security only show 1st characters
    
    # update password, this is conventional setter
    #def set_password(self, password):
     #   """Create a hashed password."""
      #  self._password = generate_password_hash(password, method='sha256')

    # check password parameter versus stored/encrypted password
    #def is_password(self, password):
     #   """Check against hashed password."""
      #  result = check_password_hash(self._password, password)
       # return result  
    
    @review.setter
    def photel(self, review):
        self._review = review
    # dob property is returned as string, to avoid unfriendly outcomes

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, activity):
        self._activity = activity

    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "review": self.review,
            "activity": self.activity,
            #"posts": [post.read() for post in self.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", rating="", review="", activity=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(rating) > 0:
            self.rating = rating
        if len(review) > 0:
            self._review = review
        if len(activity) > 0:
            self.activity = activity
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """

# Builds working data for testing
def initYelp():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        y1 = Yelp(name='Thomas Edison', rating='five', review='good', activity='seaworld')
        y2 = Yelp(name='Nicholas Tesla', rating='five', review='good', activity='del mar')
        y3 = Yelp(name='Alexander Graham Bell', rating='five', review='good', activity='petco park')
        y4 = Yelp(name='Eli Whitney',  rating='five', review='good', activity='seaworld')
        y5 = Yelp(name='John Mortensen', rating='five', review='good', activity='del mar')

        yelp = [y1, y2, y3, y4, y5]

        """Builds sample user/note(s) data"""
        for yelp in yelp:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + yelp.name + " note " + str(num) + ". \n Generated by test data."
                    yelp.put.append(Put(id=yelp.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                yelp.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {yelp.uid}")
