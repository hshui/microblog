from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import webapp
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

@webapp.route('/')
@webapp.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Vancouver!'
        },
        {
            'author': {'username': 'Donald'},
            'body': 'Someone made me mad again!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

# @webapp.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)

# View that supports GET and POST methods
@webapp.route('/login', methods=['GET', 'POST'])
def login():
    # current_user variable provided by flask_login. Value is set by user loader in models
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # processes the form. If POST request is called it will run validators attached to fields and return true if everything passes else false 
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login credentials invalid.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        #empty or next query contains a full url with domain. Latter is dangerous url redirect.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@webapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@webapp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Yay thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)