from app import db
from hashlib import md5

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# UserMixin that includes generic implementations that are appropriate for most user model classes.
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # run flask db migrate -m "new fields in user model"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        hex_email = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            hex_email, size)
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.body)

# extension expects that the application will configure a user loader function, that can be called to load a user given the ID.
from app import login # ...
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

