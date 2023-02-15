from random import randrange
from datetime import date
import os, base64 

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
import json

class Activity:
    def __init__(activity, name, hobby, price, duration):
        activity._name = name
        activity._hobby = hobby
        activity._price = price
        activity._duration = duration
        
@property 
def activity(activity):
    return activity._name

@activity.setter
def activity(activity, name):
    activity._name = name 
    
@property
def hobby(activity):
    return activity._hobby

@hobby.setter
def hobby(activity, hobby):
    activity._hobby = hobby
    
@property
def price(activity):
    return activity._price

@price.setter
def price(activity, price):
    activity._price = price
    
@property
def duration(activity):
    return activity._duration

@duration.setter
def duration(activity, duration):
    activity._duration = duration
    
# output content using str(object) in human readable form, uses getter
    def __str__(activity):
        return f'name: "{activity.name}", hobby: "{activity.hobby}", price: "{activity.price}", duration: "{activity.duration}"'
    
# output command to recreate the object, uses attribute directly
    def __repr__(activity):
        return f'Activity(name={activity._name}, hobby={activity._hobby}, price={activity._price}, duration={activity._duration})'

if __name__ == "__main__":
    
    #define activity objevts
    a1 = Activity(name='SeaWorld', hobby='park', price= "$109-$200", duration= 'all-day')
    a2 = Activity(name='Balboa Park', hobby='', price='', duration='')
    a3 = Activity(name='Del Mar Beach', hobby='', price='', duration='')
    a4 = Activity(name='La Jolla Beach', hobby='', price='', duration='')
    a5 = Activity(name='Hotel Del', hobby='', price='', duration='')
    a6 = Activity(name='', hobby='', price='', duration='')
    a7 = Activity(name='', hobby='', price='', duration='')
    a9 = Activity(name='', hobby='', price='', duration='')
    a10 = Activity(name='', hobby='', price='', duration='')
    a11 = Activity(name='', hobby='', price='', duration='')
    a12 = Activity(name='', hobby='', price='', duration='')
    a13 = Activity(name='', hobby='', price='', duration='')
    

# pur user objects in list for convenience
activities = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13]

print("Test 1, make a dictionary")
json_string = json.dumps([user.__dict__ for user in users]) 
print(json_string)
