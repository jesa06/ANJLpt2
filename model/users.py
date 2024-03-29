""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Weather(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=False, nullable=False)
    dos = db.Column(db.Date)
    # Define the Notes schema
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users._uid'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, city, dos):
        self.userID = id
        self.city = city
        self.dos = dos

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Weather(" + str(self.id) + "," + str(self.city) + "," + self.dos + "," + str(self.userID) + ")"

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
      #  path = app.config['UPLOAD_FOLDER']
       # file = os.path.join(path, self.image)
        #file_text = open(file, 'rb')
        #file_read = file_text.read()
        #file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "city": self.city,
            "dateOfSearch": self.dos
        }

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _phone = db.Column(db.String(255), unique=False, nullable=False)
    _email = db.Column(db.String(225), unique=False, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _age = db.Column(db.Integer, unique=False, nullable=True)

    weather = db.relationship('Weather', backref='user', lazy=True)


    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
   # posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, phone="8588888888", email="seanyeung@gmail.com", password="123qwerty", dob=date.today(), age=17):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._phone = phone
        self._email = email
        self._password = password
        self._dob = dob
        self._age = age

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def phone(self):
        return self._phone
    
    # a setter function, allows name to be updated after initial object creation
    @phone.setter
    def phone(self, phone):
        self._phone = phone
    
    @property
    def email(self):
        return self._email
    
    # a setter function, allows name to be updated after initial object creation
    @email.setter
    def email(self, email):
        self._email = email

    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    
    @property
    def password(self):
        return self._password[0:5] + "..." # because of security only show 1st characters

    @password.setter
    def password(self, password):
        self._password = password
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(self, dob):
        self._dob = dob
    
    @property 
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age
    
    def find_by_uid(self, uid):
        with app.app_context():
            user = User.query.filter_by(_uid=uid).first()
        return user

    def find_by_city(self, city):
        with app.app_context():
            city = Weather.query.filter_by(city=city).first()
        return city

    #def is_password(self, password):
    #     return self._password == password;        

    def is_password(self, password):        
        return (self._password, password)

   # def is_password(self, password):
    #    result = (self._password, password)
     #   return result
    # AI CODE
    #def is_password(self, password):
     #   return self.password == password

    #def check_credentials(uid, password):
        # query email and return user record
     #   user = user.find_by_uid(uid)
      #  if user == None:
        #    return False 
        #if (user.is_password(password)):
         #   return True
        #return False

    def check_credentials(self, uid, password):
        user = self.find_by_uid(uid)
        if user == None:
            return False
        if (user.is_password(password)):
            return True
        return False
        # query email and return user record
        #if self.uid == uid and self.is_password(password):
         #   return True
        #else:
         #   return False

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
            "uid": self.uid,
            "phone": self.phone,
            "email": self.email,
            "dob": self.dob,
            "age": self.age,
        }  


    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", phone="", email="", password="", dob="", age=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(phone) > 0:
            self.phone = phone
        if len(email) > 0:
            self.email = email
        if len(password) > 0:
            self.password = password
        if len(dob) > 0:
            self.dob = dob
        if len(age) > 0:
            self.age = age
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day)) 

# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Joselyn Anda2', uid='jesa06', phone='8586197777', email='joseanda@gmail.com', password='123ellyna4', dob=date(2006, 1, 15), age=calculate_age(date(2006, 1, 15)))
        u2 = User(name='Lina Awad2', uid='linaawad1', phone='8886665555', email='linaaaa@gmail.com', password='thomas82', dob=date(2006, 10, 3), age=calculate_age(date(2006, 10, 28)))
        u3 = User(name='Naja Fonseca2', uid='najaAFonseca', phone='8587360021', email='najaAF@gmail.com', password='Purpleflower0', dob=date(2007, 10, 5), age=calculate_age(date(2007, 9, 20)))
        u4 = User(name='Amitha Sanka2', uid='amitha-sanka', phone='8584320098', email='amithaaaaas@gmail.com', password='tobyyWhite3', dob=date(1959, 10, 21), age=calculate_age(date(2005, 10, 1)))

        users = [u1, u2, u3, u4]

        """Builds sample user/weather(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 20)):
                  # city = "#### " + user.name + " weather " + str(num) + ". \n Generated by test data."
                    user.weather.append(Weather(id=user.id, city=Weather.city, dos=Weather.dos))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
            


#class Weather(db.Model):
 #   __tablename__ = 'weather'

  #  id = db.Column(db.Integer, primary_key=True)
   # uid = db.Column(db.String(255), db.ForeignKey('users._uid'), nullable=False)
#    city = db.Column(db.String, unique=False, nullable=False)
 #   dos = db.Column(db.Date)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #user = db.relationship("User", back_populates="weather")
    
    # Define a relationship in Weather Schema to userID who originates the note, many-to-one (many notes to one user)
    #uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    #uid = relationship('User', back_populates='weather')


 #   @property
  #  def uid(self):
   #     return self._uid
    
    # a setter function, allows name to be updated after initial object creation
   # @uid.setter
    #def uid(self, uid):
     #   self._uid = uid

    #@property
    #def city(self):
       # return self._city
    
    # a setter function, allows name to be updated after initial object creation
    #@city.setter
    #def city(self, city):
    #    self._city = city

    #@property
    #def dos(self):
     #   return self._dos
    
    # a setter function, allows name to be updated after initial object creation
    #@dos.setter
    #def dos(self, dos):
     #   self._dos = dos

    #def __init__(self, uid, city, dos):
     #   self.uid = uid
    #    self.city = city
     #   self.dos = dos

    #def __str__(self):
     #   return json.dumps(self.read())

    #def __repr__(self):
       # return "Weather(" + str(self.id) + "," + self.city + "," + str(self.uid) + ")"

    #def create(self):
    #    try:
            # creates a Weather object from Weather(db.Model) class, passes initializers
     #       db.session.add(self)  # add prepares to persist person object to Weather table
     #       db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
      #      return self
      #  except IntegrityError:
      #      db.session.remove()
       #     return None

    # CRUD read, returns dictionary representation of Weather object
    # returns dictionary
    #def read(self):
       # return {
     #       "id": self.id,
      #      "uid": self.uid,
         #   "city": self.city,
        #    "dateOfSearch": self.dos
      #  }

    # CRUD delete: remove self
    # None
   # def delete(self):
    #    db.session.delete(self)
      #  db.session.commit()
     #   return None
#

#def initWeather():
 #   with app.app_context():
  #      db.create_all()
   #     u1 = User(name='Joselyn', uid='jesa06')
    #    db.session.add(u1)
     #   db.session.commit()
#
   #     """Tester data for table"""
 #       w1 = Weather(user=u1, city='Escondido', dos=date(2023, 1, 15))
  #      w2 = Weather(user=u1, city='Carlsbad', dos=date(2023, 3, 30))
        

   #     weathers = [w1, w2]

     #   for weather in weathers:
    #        try: 
      #          weather.create()
       #     except IntegrityError:
        #        '''fails with bad or duplicate data'''
         #       db.session.remove()
          #      print(f"Records exist, duplicate email, or error: {weather.city}")

       # """Builds sample user/note(s) data"""
       # for weather in weathers:
        #    try:
         #       '''add a few 1 to 4 weather searches per user'''
          #      for num in range(randrange(1, 2)):
           #         weather.posts.append(Weather(uid=weather.uid, city=weather.city, dos=weather.dos))
            #    weather.create()
            #except IntegrityError:
             #   '''fails with bad or duplicate data'''
              #  db.session.remove()
