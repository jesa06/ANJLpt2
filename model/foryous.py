from random import randrange
from datetime import date
import os, base64 

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import json

class Activity:
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
    def __str__(self):
        return f'name: "{self._name}", hobby: "{self._hobby}", price: "{self._price}", duration: "{self._duration}", location: "{self._location}"'
    
    # output command to recreate the object, uses attribute directly
    def __repr__(self):
        return f'Activity(name={self._name}, hobby={self._hobby}, price={self._price}, duration={self._duration}, location={self._location})'

def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
    
        a1 = Activity(name='SeaWorld', hobby='park', price= "$109-$200", duration= 'all-day', location='San Diego')
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
activities = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13]

print("Test 1, make a dictionary")
json_string = json.dumps([activity.__dict__ for activity in activities]) 
print(json_string)
