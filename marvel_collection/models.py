from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable=False, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=False, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    marvel_char = db.relationship('MarvelCharacter', backref='owner', lazy=True)

    def __init__(self, email, id='', first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"User {self.email} has been added to the database"

class MarvelCharacter(db.Model):
    id = db.Column(db.String, primary_key = True)
    superhero_name = db.Column(db.String(50), nullable=False, default='')
    name = db.Column(db.String(50), default='')
    description = db.Column(db.String(150), default='')
    num_of_comics = db.Column(db.Integer, default=1)
    superpower = db.Column(db.String(50), nullable=False, default='')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, superhero_name='', name='', description='', num_of_comics = 1, superpower='', user_token='', id=''):
        self.id = self.set_id()
        self.superhero_name = superhero_name
        self.name = name
        self.description = description
        self.num_of_comics = num_of_comics if num_of_comics else 1
        self.superpower = superpower
        self.user_token = user_token

    def __repr__(self):
        return f"The following Marvel character has been added: {self.superhero_name}"
    
    def set_id(self):
        return secrets.token_urlsafe()

class MarvelCharSchema(ma.Schema):
    class Meta:
        fields = ['id', 'superhero_name', 'name', 'description', 'num_of_comics', 'superpower']

marvel_char_schema = MarvelCharSchema()
marvel_chars_schemas = MarvelCharSchema(many=True)