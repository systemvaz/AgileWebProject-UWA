from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from datetime import datetime

from app import app
from app import db
from app.models import User, Qset, Question, Multichoice, Results, Attempts
from app.forms import LoginForm, NewQuizForm, TakeQuizForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# Routes for login and logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# ------------------------
# Quiz routes
# ------------------------

# Route to view available active Quizes
@app.route('/view_quizes')
def view_quizes():
    quizes = Qset.query.filter_by(is_active=True).all()
    return render_template('view_quizes.html', title='Available Quizes', quizes=quizes)


# Route to take user to a quiz
@app.route('/take_quiz', methods=['GET', 'POST'])
def take_quiz():
    # Get current user PK
    user_id = current_user.get_id()
    # Get the Qset id passed to route as args
    qset_id = request.args.get('quiz')
    qset = Qset.query.filter_by(id=qset_id).first()
    # Get all questions via FK
    questions = Question.query.filter_by(qset_id=int(qset_id)).all()
    multichoice = []

    # Get all related multichoice answers via FK 
    for q in questions:
        if q.get_multichoice:
            multichoice.append(Multichoice.query.filter_by(question_id=q.id).all())

    form = TakeQuizForm()
    review_flag = False
    i = 0

    # Check submitted answers and add to Results table
    if form.validate_on_submit():        
        # Add an entry to the Attempts table and get id PK for Result FK
        attempt = Attempts(user_id=user_id, qset_id=qset_id, timestamp=datetime.utcnow())
        db.session.add(attempt)
        db.session.commit()
        attempt_id = attempt.id   
        for q in questions:
            if q.get_multichoice():
                # Check if multichoice answer is correct or not and add results to Result table
                mc_id = form.answer_for_q[i].data.get("answer")
                mc = Multichoice.query.filter_by(id=mc_id).first()
                is_correct = mc.is_correct
                result = Results(user_id=user_id, qset_id=qset_id, attempt_id=attempt_id, question_id=q.id, answer_mc=mc_id, answer_txt=None, is_needs_review=False, is_correct=is_correct)
                # print("{} | {} | {} | {} | {} | {} | {}".format(result.user_id, result.qset_id, result.question_id, result.answer_mc, result.answer_txt, result.is_needs_review, result.is_correct), flush=True)
                db.session.add(result)
                db.session.commit()
            elif not q.get_multichoice():
                # Not multichoice so needs to be flagged for admin review. Add to Result table
                review_flag = True
                answer_txt = form.answer_for_q[i].data.get("answer")
                result = Results(user_id=user_id, qset_id=qset_id, attempt_id=attempt_id, question_id=q.id, answer_mc=None, answer_txt=answer_txt, is_needs_review=True, is_correct=None)
                # print("{} | {} | {} | {} | {} | {} | {}".format(result.user_id, result.qset_id, result.question_id, result.answer_mc, result.answer_txt, result.is_needs_review, result.is_correct), flush=True)
                db.session.add(result)
                db.session.commit()
            i += 1     
    
    return render_template('render_quiz.html', title='Take this Quiz', quiz=qset, questions=questions, multichoice=multichoice, form=form)


# ------------------------
# Administrator routes
# ------------------------

# Route to Administrator panel
@app.route('/admin')
def admin():
    if current_user.is_anonymous or current_user.is_admin != True:
        return redirect(url_for('index')) 
    
    return render_template('/admin/index.html', title='Administrator Panel')


# Route to create new QnA set: admin/new_quiz
@app.route('/admin/new_quiz', methods=['GET', 'POST'])
def admin_newquiz():
    if current_user.is_anonymous or current_user.is_admin != True:
        return redirect(url_for('index'))   

    form = NewQuizForm()
    if form.validate_on_submit():
        # Commit new quiz to Qset and obtain PK
        qset = Qset(title=form.title.data, is_active=True)
        db.session.add(qset)
        db.session.commit()
        qset = Qset.query.filter_by(title=form.title.data).first()
        qset_id = qset.id
        
        i = 0
        for q in form.questions:
            print(q.multichoice.data, flush=True)
            if q.multichoice.data == 'True':
                # Adding Multiple Choice question to Question table. Commit and get PK
                question = Question(qset_id=qset_id, question=q.question.data, is_multichoice=True)
                db.session.add(question)
                db.session.commit()
                question = Question.query.filter_by(question=q.question.data).first()
                question_id = question.id

                ans = form.answers[i]
                correct = int(ans.correct.data)
                set_correct = False
                # Adding multichoice answer 1 to Multichoice table
                print('Adding answer 1: {}'.format(ans.answer1.data))
                if correct == 0: set_correct = True
                else: set_correct = False
                mc = Multichoice(question_id=question_id, answer_selection=ans.answer1.data, is_correct=set_correct)
                db.session.add(mc)
                # Adding multichoice answer 2 to Multichoice table
                print('Adding answer 2: {}'.format(ans.answer2.data))
                if correct == 1: set_correct = True
                else: set_correct = False
                mc = Multichoice(question_id=question_id, answer_selection=ans.answer2.data, is_correct=set_correct)
                db.session.add(mc)
                # Adding multichoice answer 3 to Multichoice table
                print('Adding answer 3: {}'.format(ans.answer3.data))
                if correct == 2: set_correct = True
                else: set_correct = False
                mc = Multichoice(question_id=question_id, answer_selection=ans.answer3.data, is_correct=set_correct)
                db.session.add(mc)
                # Adding multichoice answer 4 to Multichoice table
                print('Adding answer 4: {}'.format(ans.answer4.data))
                if correct == 3: set_correct = True
                else: set_correct = False
                mc = Multichoice(question_id=question_id, answer_selection=ans.answer4.data, is_correct=set_correct)
                db.session.add(mc)
                db.session.commit()
                i = i + 1
            elif q.multichoice.data == 'False':
                # Adding Non-Multichoice question to Question table
                question = Question(qset_id=qset_id, question=q.question.data, is_multichoice=False)
                db.session.add(question)
                db.session.commit()

        return redirect(url_for('admin'))

        flash(form.questions.data + form.answers.data)

    return render_template('/admin/newquiz.html', title='Create a new Quiz!', form=form)