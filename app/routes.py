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
    quizes = Qset.query.filter_by(is_active=True).all()
    return render_template('index.html', title='Home', quizes=quizes)

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
    # Get some stats on all the quizes
    attempts = []
    user_attempts = []
    for q in quizes:
        attempts_check = Attempts.query.filter_by(qset_id=q.id).all()
        user_check = Attempts.query.filter_by(qset_id=q.id, user_id=current_user.id).all()
        attempts.append(len(attempts_check))
        user_attempts.append(len(user_check))
        print(len(user_check))


    return render_template('view_quizes.html', title='Available Quizes', quizes=quizes, attempts=attempts, user_attempts=user_attempts)


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

            attempt.is_needs_review = review_flag
            db.session.add(attempt)
            db.session.commit()

        attempt_id = attempt.id
        user = User.query.filter_by(id=user_id).first()
        user = user.username
        return redirect(url_for('reviewquiz', attempt=attempt_id, user=user))     
    
    return render_template('render_quiz.html', title='Take this Quiz', quiz=qset, questions=questions, multichoice=multichoice, form=form)


# Route to review quiz with marks. If admin allows for marking of quiz.
@app.route('/review_quiz', methods=['GET', 'POST'])
def reviewquiz():
    # if current_user.is_anonymous or current_user.is_admin != True:
    #     return redirect(url_for('index'))   

    attempt_id = request.args.get('attempt')
    user = request.args.get('user')

    attemptquery = Attempts.query.filter_by(id=attempt_id).first()
    timestamp = attemptquery.timestamp
    timestamp = timestamp.strftime("%A %d, %B %Y @ %H:%M")
    qset_id = attemptquery.qset_id

    qset = Qset.query.filter_by(id=qset_id).first()
    qset = qset.title
    
    questions = Question.query.filter_by(qset_id=qset_id).all()
    answers = Results.query.filter_by(attempt_id=attempt_id).all()
    mc_txt = []

    for a in answers:
        if not a.answer_mc is None:
            mc = Multichoice.query.filter_by(id=a.answer_mc).first()
            print(mc.answer_selection, flush=True)
            mc_txt.append(mc.answer_selection)

    # Run actions when question is marked correct or wrong by pressing the buttons
    if request.method == 'POST':
        markCorrect = request.form.get('markCorrect')
        markWrong = request.form.get('markWrong')
        
        if markCorrect is not None:
            mark = Results.query.filter_by(attempt_id=attempt_id, question_id=markCorrect).first()
            mark.is_correct = True
        elif markWrong is not None:
            mark = Results.query.filter_by(attempt_id=attempt_id, question_id=markWrong).first()
            mark.is_correct = False

        mark.is_needs_review = False
        db.session.add(mark)
        db.session.commit()

        # Check if there are any more questions to mark, if not change is_needs_review flag and return to admin page
        mark_check = Results.query.filter_by(attempt_id=attempt_id, is_needs_review=True).all()
        print("mark check: {}".format(mark_check))
        if not mark_check:
            mark_complete = Attempts.query.filter_by(id=attempt_id).first()
            mark_complete.is_needs_review = False
            db.session.add(mark_complete)
            db.session.commit()

            return redirect(url_for('admin'))

    return render_template('review_quiz.html', title="Review this Quiz", user=user, timestamp=timestamp, qset=qset, questions=questions, answers=answers, mc_txt=mc_txt)

# Helper funtion to return quiz attempts, marks and stats given a user id
def helper_get_results(user_id):
    quiz = []
    qset_ids = []
    mark = []
    mark_outof = []
    pending = []
    attempt_ids = []
    timestamp = []
    i = 0

    user_attempts = Attempts.query.filter_by(user_id=user_id).all()

    for a in user_attempts:
        q_count = 0
        correct_count = 0
        qset_ids.insert(i, a.qset_id)
        result = Results.query.filter_by(attempt_id=a.id).all()
        quiz_title = Qset.query.filter_by(id=a.qset_id).first()
        quiz.insert(i, quiz_title.title)
        pending.insert(i, a.is_needs_review)
        attempt_ids.insert(i, a.id)
        time = a.timestamp
        time = time.strftime("%A %d, %B %Y @ %H:%M")
        timestamp.insert(i, time)
        
        for r in result:
            is_correct = r.is_correct
            if is_correct:
                correct_count += 1
            mark.insert(i, correct_count)
            q_count += 1
            mark_outof.insert(i, q_count)

        i = i + 1

    return qset_ids, quiz, mark, mark_outof, pending, attempt_ids, timestamp



# Route for a user to view all of their results, calls above helper function
@app.route('/review_results')
def review_results():
    user_id = 0
    if request.args.get('user') is None:
        user_id = current_user.id
    else:
        user_id = request.args.get('user')
    _, quiz, mark, mark_outof, pending, attempt_ids, timestamp = helper_get_results(user_id)

    return render_template('review_results.html', title="View your Results", quiz=quiz, mark=mark, mark_outof=mark_outof, pending=pending, attempts=attempt_ids, timestamp=timestamp)


# Helper function to return the best result a user obtained for each quiz they attempted
def helper_get_topmark(qset_ids, mark, mark_outof, pending):
    i = 0
    exists = False
    top_mark_dict = []

    for qset in qset_ids:
        if not pending[i]:
            get_mark = mark[i]
            get_outof = mark_outof[i]
            for check in top_mark_dict:
                if check.get("qset_id") == qset:
                    # Check if this entry if the top mark seen so far
                    exists = True
                    if check.get("top_mark") < get_mark:
                        check["top_mark"] = get_mark
            if not exists:
                top_mark_dict.append({"qset_id": qset, "top_mark": get_mark, "out_of": get_outof})    
        exists = False    
        i = i + 1        

    return top_mark_dict


# Route to view the leaderboard for all quizes, calls above helper function
@app.route('/view_ladder')
def view_ladder():
    exists = False
    # Leaderboard dictionary
    leaderboard_dict_lst = []

    all_users = User.query.all()
    # Get results and their top marks for each user
    for user in all_users:
        username = user.username
        qset_id, quiz, mark, mark_outof, pending, attempt_ids, timestamp = helper_get_results(user.id)
        user_mark_dict = helper_get_topmark(qset_id, mark, mark_outof, pending)
        
        # Do comparison with our Leaderboard dictionary.
        for user_mark in user_mark_dict:
            for check in leaderboard_dict_lst:
                # If quiz id in leaderboard dict, check if users top mark is the global top mark seen so far
                if check.get("qset_id") == user_mark.get("qset_id"):
                    exists = True
                    if check.get("top_mark") < user_mark.get("top_mark"):
                        # Add it to our Leaderboard dict
                        check["user"] = username
                        check["mark"] = user_mark.get("top_mark")
                        check["out_of"] = user_mark.get("mark_outof")
                    
            # If no entry for this quiz in leaderboard dict so far OR the user got equal top marks with another user.
            # Add to our leaderboard dict
            if not exists or check.get("top_mark") == user_mark.get("top_mark"):
                leaderboard_dict_lst.append({"user": username, "qset_id": user_mark.get("qset_id"), "top_mark": user_mark.get("top_mark"), "out_of": user_mark.get("out_of")})
            exists = False

    qsets = Qset.query.all()

    return render_template('view_ladder.html', title='Leaderboards', leaderboard=leaderboard_dict_lst, qsets=qsets)

    

# ------------------------
# Administrator routes
# ------------------------

# Route to Administrator panel
@app.route('/admin')
def admin():
    if current_user.is_anonymous or current_user.is_admin != True:
        return redirect(url_for('index')) 

    # Get all quizes needing administrator review
    review_quizes = Attempts.query.filter_by(is_needs_review=True).all()
    # Get user and question set info for these
    review_user = []
    review_qset = []
    for r in review_quizes:
        userquery = User.query.filter_by(id=r.user_id).first()
        review_user.append(userquery.username)
        qsetquery = Qset.query.filter_by(id=r.qset_id).first()
        review_qset.append(qsetquery.title)

    users = User.query.all()
    
    return render_template('/admin/index.html', title='Administrator Panel', review_quizes=review_quizes, review_users=review_user, review_qset=review_qset, users=users)


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

    return render_template('/admin/new_quiz.html', title='Create a new Quiz!', form=form)
