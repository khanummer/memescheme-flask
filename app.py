from flask import Flask, g, render_template, flash, redirect, url_for
from resources.memes import memes_api
from resources.users import users_api
# from resources.login import login_api

import models
from flask_restful import reqparse

from flask_wtf import FlaskForm as form
from wtforms import (StringField, PasswordField, TextAreaField)

from wtforms.validators import (DataRequired, ValidationError, Email, Length, EqualTo)

from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
login_manager = LoginManager()

import os 

from werkzeug.utils import secure_filename

import config




app = Flask(__name__)
app.secret_key = config.SECRET_KEY
CORS(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user
    print(g.user,'g.user')
    
@app.after_request
def after_request(response):
    g.db.close()
    return response

CORS(memes_api, origins=["http://memeschemeapp.herokuapp.com", "http://memescheme.herokuapp.com"], supports_credentials=True)
CORS(users_api, origins=["http://memeschemeapp.herokuapp.com", "http://memescheme.herokuapp.com"], supports_credentials=True)
# CORS(login_api, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(memes_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')
# app.register_blueprint(login_api, url_prefix='/api/v1')


# @app.route('/register', methods=('GET', 'POST'))
# def register():
#     form = forms.registerForm()



@app.route('/')
def hello_world():
    return 'Hello World'


if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
    

