from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Define our dimension tables
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_admin(self):
        return self.admin

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

class Multichoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_selection = db.Column(db.String(128))
    is_correct = db.Column(db.Boolean)  

class Attempted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qset_id = db.Column(db.Integer, db.ForeignKey('qset.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_txt = db.Column(db.String(256))
    answer_mc = db.Column(db.Integer, db.ForeignKey('multichoice.id'))
    is_correct = db.Column(db.Boolean)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))