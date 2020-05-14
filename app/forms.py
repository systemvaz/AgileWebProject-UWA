from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Administrator forms
class MultiChoiceForm(FlaskForm):
    answer1 = StringField('Answer 1')
    answer2 = StringField('Answer 2')
    answer3 = StringField('Answer 3')
    answer4 = StringField('Answer 4')
    correct = StringField('Correct Answer')

class QuestionsForm(FlaskForm):
    question = StringField('Question')
    multichoice  = StringField('Multichoice')

class NewQuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired()])
    # questions = FieldList(StringField('Question', validators=[DataRequired()]), min_entries=1)
    questions = FieldList(FormField(QuestionsForm), min_entries=1, max_entries=4, validators=None)
    answers = FieldList(FormField(MultiChoiceForm), min_entries=1, max_entries=4, validators=None)
    submit = SubmitField('Create Quiz!')