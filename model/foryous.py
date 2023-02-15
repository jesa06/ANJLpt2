from random import randrange
from datetime import date
import os, base64 

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import json

class Activity:
    def __init__(self, name, hobby, price, duration):
        self._name = name
        self._hobby = hobby
        self._price = price
        self._duration = duration
        
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
    
# output content using str(object) in human readable form, uses getter
def __str__(self):
    return f'name: "{self._name}", hobby: "{self._hobby}", price: "{self._price}", duration: "{self._duration}"'
    
# output command to recreate the object, uses attribute directly
def __repr__(self):
    return f'Activity(name={self._name}, hobby={self._hobby}, price={self._price}, duration={self._duration})'

if __name__ == "__main__":
    
    #define activity objects
    a1 = Activity(name='SeaWorld', hobby='park', price= "$109-$200", duration= 'all-day')
    a2 = Activity(name='Balboa Park', hobby='', price='', duration='')
    a3 = Activity(name='Del Mar Beach', hobby='', price='', duration='')
    a4 = Activity(name='La Jolla Beach', hobby='', price='', duration='')
    a5 = Activity(name='Hotel Del', hobby='', price='', duration='')
    a6 = Activity(name='', hobby='', price='', duration='')
    a7 = Activity(name='', hobby='', price='', duration='')
    a8 = Activity(name='', hobby='', price='', duration='')
    a9 = Activity(name='', hobby='', price='', duration='')
    a10 = Activity(name='', hobby='', price='', duration='')
    a11 = Activity(name='', hobby='', price='', duration='')
    a12 = Activity(name='', hobby='', price='', duration='')
    a13 = Activity(name='', hobby='', price='', duration='')   

# pur user objects in list for convenience
activities = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13]

print("Test 1, make a dictionary")
json_string = json_string = json.dumps([activity.__dict__ for activity in activities]) 
print(json_string)
