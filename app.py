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
# login_manager.login_view = 'login'

# CORS placement here

app.register_blueprint(memes_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')


@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
    

