from flask import render_template, flash, redirect
from app import webapp
from app.forms import LoginForm

@webapp.route('/')
@webapp.route('/index')

def index():
    user = {'username': 'Herman'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

# @webapp.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)

# View that supports GET and POST methods
@webapp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # processes the form. If POST request is called it will run validators attached to fields and return true if everything passes else false 
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)