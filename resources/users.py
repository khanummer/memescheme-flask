import json

from flask import jsonify, Blueprint, abort 

from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)

from flask_login import login_user, logout_user

import models

user_fields = {
    'username': fields.String
}

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No verify_password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'memes',
            required=True,
            help='No memes provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'favs',
            required=True,
            help='No favs provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )

        super().__init__()



    def get(self):
        users=[ marshal(user, user_fields) for user in models.User.select() ]
        return {'users': users}

    def post(self):
        args = self.reqparse.parse_args()
        print(args, 'args in post route USERS')
        if args['password'] == args['verify_password']:
            user = models.User.create_user(username = args['username'], password=['password'], email=['email'], memes=['memes'], favs=['favs'])
            login_user(user)
            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                'error': 'passwords do not match'
            }), 400
        )

    

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)