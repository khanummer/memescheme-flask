import json

from flask import jsonify, Blueprint, abort 

from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)

from flask_login import login_user, logout_user, current_user, LoginManager

login_manager = LoginManager()

from flask_bcrypt import check_password_hash

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

class User(Resource):
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

    @marshal_with(user_fields)
    def get(self, id):
        return user_or_404(id)

    @marshal_with(user_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.User.update(username = args['username'], password=args['password'], email=args['email'], is_admin=args['is_admin']).where(models.User.id == id)
        query.execute()
        return(models.User.get(models.User.id == id), 200)

    def delete(self, id):
        query = models.User.delete().where(models.User.id == id)
        query.execute()
        return ('USER DELETED')

class UserLogin(Resource):
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

        super().__init__()
# try this catch
    def post(self):
        args = self.reqparse.parse_args()
        print(args['username'])
        print(args)
        try:
            logged_user = models.User.get(models.User.username == args['username'])
            return marshal(logged_user, user_fields)
        except:
            return "wrong"


    # def post(self):
    #     args = self.reqparse.parse_args()
    #     if args.validate_on_submit():
    #         try:
    #             user = models.User.get(
    #                 models.User.email == args.email.data
    #             )
    #             if check_password_hash(user.password, args.password.data):
    #                 login_user(user)
    #                 print("You're now logged in!")
    #             else:
    #                 print("No user with that email/password combo")
    #         except models.DoesNotExist:
    #             print("No user with that email/password combo")
    #     return render_template('register.html', args=args) 

    # def post(self):
    #     args = self.reqparse.parse_args()
    #     print(args['username'])
    #     print(models.User.get(models.User.password), 'models password')
    #     print(args['password'], 'args password')
        # if models.User.get(models.User.password == args['password']):
            # logged_user = models.User.get(models.User.username == args['username'])
            # print('---------- logged')
            # if logged_user:
            #     login_user(logged_user)
            #     print(current_user)
            #     print('current_user')
            #     return marshal(logged_user, user_fields)
        # else:
            # return 'YOUR PASSWORD IS WRONG'

    

users_api = Blueprint('resources.users', __name__)
api = Api(users_api)


api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
api.add_resource(
    UserLogin,
    '/users/login',
    endpoint='userlogin'
)
api.add_resource(
    User,
    '/users/<int:id>',
    endpoint='user'
)

