from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Administrator forms

class NewQuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired()])
    questions = FieldList(StringField('Question', validators=[DataRequired()]), min_entries=1)
    submit = SubmitField('Create Quiz!')