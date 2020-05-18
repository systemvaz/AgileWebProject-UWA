from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Forms for taking a quiz
class TakeQuizAnswerForm(FlaskForm):
    class Meta:
        csrf = False
    answer = StringField('Answer', validators=[DataRequired()])

class TakeQuizForm(FlaskForm):
    class Meta:
        csrf = False
    answer_for_q = FieldList(FormField(TakeQuizAnswerForm), min_entries=1, validators=None)
    submit = SubmitField('Submit Your Answers!')


# ------------------------------------
# Administrator forms
# ------------------------------------

# Start: /admin/new_quiz forms
class MultiChoiceForm(FlaskForm):
    class Meta:
        csrf = False
    answer1 = StringField('Answer 1')
    answer2 = StringField('Answer 2')
    answer3 = StringField('Answer 3')
    answer4 = StringField('Answer 4')
    correct = StringField('Correct Answer')

class QuestionsForm(FlaskForm):
    class Meta:
        csrf = False
    question = StringField('Question')
    multichoice  = StringField('Multichoice')

class NewQuizForm(FlaskForm):
    class Meta:
        csrf = False
    title = StringField('Quiz Title', validators=[DataRequired()])
    questions = FieldList(FormField(QuestionsForm), min_entries=1, validators=None)
    answers = FieldList(FormField(MultiChoiceForm), min_entries=1, validators=None)
    submit = SubmitField('Create Quiz!')
# End: /admin/new_quiz forms