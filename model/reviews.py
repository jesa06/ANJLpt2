""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

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
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _activity = db.Column(db.String(255), unique=False, nullable=False)
    _rating = db.Column(db.String(225), unique=False, nullable=False)
    _review = db.Column(db.String(255), unique=False, nullable=False)
    _recommend = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, activity="seaworld", rating="five", review="super good", recommend="yes"):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._activity = activity
        self._rating = rating
        self._review = review
        self._recommend = recommend

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def activity(self):
        return self._activity
    
    # a setter function, allows name to be updated after initial object creation
    @activity.setter
    def activity(self, activity):
        self._activity = activity
    
    @property
    def rating(self):
        return self._rating
    
    # a setter function, allows name to be updated after initial object creation
    @rating.setter
    def rating(self, rating):
        self._rating = rating

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
    def review(self):
        return self._review

    @review.setter
    def review(self, review):
        self._review = review
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def recommend(self):
        return self._recommend

    @recommend.setter
    def recommend(self, recommend):
        self._recommend = recommend
    
    
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
            "activity": self.activity,
            "rating": self.rating,
            "review": self.review,
            "recommend": self.recommend,
        }



    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", activity="", rating="", review="", recommend=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(activity) > 0:
            self.activity = activity
        if len(rating) > 0:
            self.rating = rating
        if len(review) > 0:
            self.review = review
        if len(recommend) > 0:
            self.recommend = recommend
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
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Joselyn Anda', uid='jesa06', activity='seaworld', rating='five', review='super good', recommend='yes')
        u2 = User(name='Lina Awad', uid='linaawad1', activity='seaworld', rating='two', review='not super good', recommend='no')
        u3 = User(name='Naja Fonseca', uid='najaAFonseca', activity='seaworld', rating='one', review='not good', recommend='no')
        u4 = User(name='Amitha Sanka', uid='amitha-sanka', activity='seaworld', rating='three', review='okay good', recommend='yes')

        users = [u1, u2, u3, u4]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add a few 1 to 4 notes per user'''
                for num in range(randrange(1, 4)):
                    note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                    user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
                '''add user/post data to table'''
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {user.uid}")
            