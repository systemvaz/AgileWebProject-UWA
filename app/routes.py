from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import app
from app.models import User
from app.forms import LoginForm, NewQuizForm

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
# Administrator routes
# ------------------------

@app.route('/admin')
def admin():
    if current_user.is_anonymous or current_user.is_admin != True:
        return redirect(url_for('index')) 
    
    return render_template('/admin/index.html', title='Administrator Panel')

# Route to create new QnA set: admin/newqna
@app.route('/admin/new_quiz', methods=['GET', 'POST'])
def admin_newquiz():
    if current_user.is_anonymous or current_user.is_admin != True:
        return redirect(url_for('index'))   

    form = NewQuizForm()
    if form.validate_on_submit():
        for q in form.questions.data:
            print(q, flush=True)
        flash(form.questions.data)

    return render_template('/admin/newquiz.html', title='Create a new Quiz!', form=form)