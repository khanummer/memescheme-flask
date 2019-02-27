import json

from flask import jsonify, Blueprint, abort 

from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)

from flask_login import login_user, logout_user

import models

meme_fields = {
    'id': fields.Integer,
    'image': fields.String,
    'top_text': fields.String,
    'bottom_text': fields.String,
    'votes': fields.Integer,
    'created_by': fields.String
}

def meme_or_404(meme_id): 
    try:
        meme = models.Meme.get(models.Meme.id == meme_id)
    except models.Meme.DoesNotExist:
        abort(404)
    else:
        return meme



class MemeList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'image',
            required = True,
            help = 'no image provided',
            location = ['form', 'json']
            
        )
        self.reqparse.add_argument(
            'top_text',
            required = True,
            help = 'no top_text provided',
            location = ['form', 'json'],
        )
        self.reqparse.add_argument(
            'bottom_text',
            required = True,
            help = 'no bottom_text provided',
            location = ['form', 'json'],
        )
        self.reqparse.add_argument(
            'votes',
            required = True,
            help = 'no votes provided',
            location = ['form', 'json'],
        )
        self.reqparse.add_argument(
            'created_by',
            required = True,
            help = 'no created_by provided',
            location = ['form', 'json'],
        )

        super().__init__()

    def get(self):
        memes = [marshal(meme, meme_fields) for meme in models.Meme.select()]
        return {'memes' : memes}
    
    @marshal_with(meme_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, " This is args in post route")
        meme = models.Meme.create(**args)
        return meme

class Meme(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'image',
            required = True,
            help = 'no image provided',
            location = ['form', 'json'],
            
        )
        self.reqparse.add_argument(
            'top_text',
            required = True,
            help = 'no top_text provided',
            location = ['form', 'json'],
        )
        self.reqparse.add_argument(
            'bottom_text',
            required = True,
            help = 'no bottom_text provided',
            location = ['form', 'json'],
        )
        self.reqparse.add_argument(
            'votes',
            required = True,
            help = 'no votes provided',
            location = ['form', 'json'],
        )

    @marshal_with(meme_fields)
    def get(self, id):
        return meme_or_404(id)

    




memes_api = Blueprint('resources.memes', __name__)

api = Api(memes_api)

api.add_resource(
    MemeList,
    '/memes',
    endpoint = 'memes'
)

api.add_resource(
    Meme,
    '/memes/<int:id>',
    endpoint = 'meme'
)