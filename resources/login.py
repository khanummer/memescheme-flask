import json

from flask import jsonify, Blueprint, abort 

from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)

from flask_login import login_user, logout_user

import models

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
}

def user_or_404(user_id): 
    try:
        user = models.User.get(models.User.id == user_id)
    except models.User.DoesNotExist:
        abort(404)
    else:
        return user

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
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'is_admin',
            required=True,
            help='No is_admin provided',
            location=['form', 'json']
        )

        super().__init__()



    def get(self):
        users=[ marshal(user, user_fields) for user in models.User.select() ]
        return {'users': users}

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:    
            user = models.User.create_user(username = args['username'], password=args['password'], email=args['email'], is_admin=args['is_admin'])
            login_user(user)
            # print('user', user.username, user.id)
            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                'error': 'passwords do not match'
            }), 400
        )

login_api = Blueprint('resources.login', __name__)
api = Api(login_api)

api.add_resource(
    UserList,
    '/login',
    endpoint='login'
)

# api.add_resource(
#     User,
#     '/login/<int:id>',
#     endpoint='login'
# )