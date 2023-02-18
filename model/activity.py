from random import randrange
from datetime import date
import os, base64 

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import json

#class Post(db.Model):
#   __tablename__ = 'post'

    # Define the Notes schema

#    note = db.Column(db.Text, unique=False, nullable=False)
#    image = db.Column(db.String, unique=False)
        
    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
#    def read(self):
#        # encode image
#        path = app.config['UPLOAD_FOLDER']
#        file = os.path.join(path, self.image)
#        file_text = open(file, 'rb')
#        file_read = file_text.read()
#        file_encode = base64.encodebytes(file_read)
        
#        return {
#           "name": self.name,
#            "note": self.note,
#            "image": self.image,
#            "base64": str(file_encode)
#        }

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Activity(db.Model):
    __tablename__ = 'activity'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _hobby = db.Column(db.String(255), unique=True, nullable=False)
    _price = db.Column(db.String(255), unique=False, nullable=False)
    _duration = db.Column(db.String(225), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)

    def __init__(self, name, hobby, price, duration, location=''):
        self._name = name
        self._hobby = hobby
        self._price = price
        self._duration = duration
        self._location = location
        
    @property 
    def activity(self):
        return self._name

    @activity.setter
    def activity(self, name):
        self._name = name 
    
    @property
    def hobby(self):
        return self._hobby

    @hobby.setter
    def hobby(self, hobby):
        self._hobby = hobby
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price
    
    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location
        
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
            "name": self.name,
            "hobby": self.hobby,
            "price": self.price,
            "duration": self.duration,
            "location": self.location
        }
    
    # output content using str(object) in human readable form, uses getter
    def __str__(self):
        return f'name: "{self._name}", hobby: "{self._hobby}", price: "{self._price}", duration: "{self._duration}", location: "{self._location}"'
    
    # output command to recreate the object, uses attribute directly
    def __repr__(self):
        return f'Activity(name={self._name}, hobby={self._hobby}, price={self._price}, duration={self._duration}, location={self._location})'

def initActivities():
    with app.app_context():
        """Create database and tables"""
        
        db.create_all()
        db.init_app(app)
        a1 = Activity(name='SeaWorld', hobby='park', price= "$109-$200", duration= 'all-day', location='San Diego')
        a1.create()
        a2 = Activity(name='Balboa Park', hobby='', price='', duration='', location='San Diego')
        a3 = Activity(name='Del Mar Beach', hobby='', price='', duration='', location='Del Mar')
        a4 = Activity(name='La Jolla Beach', hobby='', price='', duration='', location='La Jolla')
        a5 = Activity(name='Hotel Del', hobby='', price='', duration='', location='Coronado')
        a6 = Activity(name='', hobby='', price='', duration='', location='')
        a7 = Activity(name='', hobby='', price='', duration='', location='')
        a8 = Activity(name='', hobby='', price='', duration='', location='')
        a9 = Activity(name='', hobby='', price='', duration='', location='')
        a10 = Activity(name='', hobby='', price='', duration='', location='')
        a11 = Activity(name='', hobby='', price='', duration='', location='')

        # pur user objects in list for convenience
        activities = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11] 