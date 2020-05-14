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
    class Meta:
        csrf = False
    answer1 = StringField('Answer 1', validators=[DataRequired()])
    answer2 = StringField('Answer 2', validators=[DataRequired()])
    answer3 = StringField('Answer 3', validators=[DataRequired()])
    answer4 = StringField('Answer 4', validators=[DataRequired()])
    correct = StringField('Correct Answer', validators=[DataRequired()])

class QuestionsForm(FlaskForm):
    class Meta:
        csrf = False
    question = StringField('Question', validators=[DataRequired()])
    multichoice  = StringField('Multichoice', validators=[DataRequired()])

class NewQuizForm(FlaskForm):
    class Meta:
        csrf = False
    title = StringField('Quiz Title', validators=[DataRequired()])
    questions = FieldList(FormField(QuestionsForm), min_entries=1, validators=None)
    answers = FieldList(FormField(MultiChoiceForm), min_entries=1, validators=None)
    submit = SubmitField('Create Quiz!')