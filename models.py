from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(20)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Rsvp (db.Model):
    id = db.Column(db.String, primary_key = True)
    guest_1 = db.Column(db.String(100), nullable = False)
    guest_2 = db.Column(db.String(100), nullable = True)
    message = db.Column(db.String(500), nullable = True)
    rvsp_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, message, guest_1, guest_2, id='' ):
        self.id = self.set_id()
        self.guest_1 = guest_1
        self.guest_2 = guest_2
        self.message = message

    def __repr__(self):
        return print(f'The following RSVP has been added to the database: {self.id}')

    def set_id(self):
        return (secrets.token_urlsafe())
    
class RsvpSchema(ma.Schema):
    class Meta:
        fields = ['id', 'guest_1','guest_2', 'message']

rsvp_schema = RsvpSchema()
rsvps_schema = RsvpSchema(many=True)