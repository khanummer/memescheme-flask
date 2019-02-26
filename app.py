from flask import Flask
from resources.memes import memes_api
import models
from flask_cors import CORS
from flask_login import login_manager

import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

app.register_blueprint(memes_api, url_prefix='/api/v1')


@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)
    

