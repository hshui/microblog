from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


webapp = Flask(__name__)
webapp.config.from_object(Config)
db = SQLAlchemy(webapp)
migrate = Migrate(webapp, db)
login = LoginManager(webapp)
# provides name of endpoint that will be used for url_for() call
login.login_view = 'login'
from app import routes, models, errors

if not webapp.debug:
    if webapp.config['MAIL_SERVER']:
        auth = None
        if webapp.config['MAIL_USERNAME'] or webapp.config['MAIL_PASSWORD']:
            auth = (webapp.config['MAIL_USERNAME'], webapp.config['MAIL_PASSWORD'])
        secure = None
        if webapp.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(webapp.config['MAIL_SERVER'], webapp.config['MAIL_PORT']),
            fromaddr='no-reply@' + webapp.config['MAIL_SERVER'],
            toaddrs=webapp.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        webapp.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                        backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    webapp.logger.addHandler(file_handler)

    webapp.logger.setLevel(logging.INFO)
    webapp.logger.info('Microblog startup')
