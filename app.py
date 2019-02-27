from flask import Flask
from resources.memes import memes_api
from resources.users import users_api
import models


from flask_cors import CORS
from flask_login import LoginManager, current_user
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

CORS(memes_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins=["http://localhost:3000"], supports_credentials=True)

app.register_blueprint(memes_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')


@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
    

