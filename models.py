from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the database"""
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.String(20), nullable=False, unique=True)
    
    password = db.Column(db.Text, nullable=False)
    
    email = db.Column(db.String(50), nullable=False, unique=True)
    
    first_name = db.Column(db.String(30), nullable=False)
    
    last_name = db.Column(db.String(30), nullable=False)
    
    @classmethod
    def register(cls, username, pword, email, first_name, last_name):
        """Register user with hashed password & return user."""
        hashed = bcrypt.generate_password_hash(pword)
        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pword):
        """Validate that user exists & passwords is correct. Return user if valid; else return False"""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pword):
            return user
        else:
            return False
        
class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.String(100), nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    
    username = db.Column(db.String(20), db.ForeignKey('users.username'))
    user = db.relationship('User', backref='feedback')