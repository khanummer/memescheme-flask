from flask import Flask, g, render_template, flash, redirect, url_for
from resources.memes import memes_api
from resources.users import users_api
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

CORS(memes_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(memes_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')

# @app.route('/register', methods=('GET', 'POST'))
# def register():
#     form = forms.registerForm()



@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/api/v1/login', methods=['GET', 'POST'])

def login():
    login_user(current_user)
    print(current_user)

# def login():
#     # # Here we use a class of some kind to represent and validate our
#     # # client-side form data. For example, WTForms is a library that will
#     # # handle this for us, and we use a custom LoginForm to validate.
#     # # form = 
#     # if form.validate_on_submit():
#     #     # Login and validate the user.
#     #     # user should be an instance of your `User` class
#     #     login_user(user)

#     #     flask.flash('Logged in successfully.')

#     #     next = flask.request.args.get('next')
#     #     # is_safe_url should check if the url is safe for redirects.
#     #     # See http://flask.pocoo.org/snippets/62/ for an example.
#     #     if not is_safe_url(next):
#     #         return flask.abort(400)

#     #     return flask.redirect(next or flask.url_for('index'))
#     # return flask.render_template('login.html', form=form)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
    

