from app import db, login
from hashlib import md5
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# DB dimension tables
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def check_admin(self):
        return self.admin
    def get_id(self):
        return self.id
    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Qset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    is_active = db.Column(db.Boolean)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qset_id = db.Column(db.Integer, db.ForeignKey('qset.id'))
    question = db.Column(db.String(256))
    is_multichoice = db.Column(db.Boolean)

    def get_multichoice(self):
        return self.is_multichoice

class Multichoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_selection = db.Column(db.String(128))
    is_correct = db.Column(db.Boolean)  

class Attempts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qset_id = db.Column(db.Integer, db.ForeignKey('qset.id'))
    is_needs_review = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

# DB Fact table
class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qset_id = db.Column(db.Integer, db.ForeignKey('qset.id'))
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_txt = db.Column(db.String(256))
    answer_mc = db.Column(db.Integer, db.ForeignKey('multichoice.id'))
    is_needs_review = db.Column(db.Boolean)
    is_correct = db.Column(db.Boolean)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))