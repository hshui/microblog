from flask import render_template
from app import webapp

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