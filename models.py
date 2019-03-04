import os

from playhouse.db_url import connect

DATABASE = connect(os.environ.get('memes.sqlite'))


import datetime

from peewee import *

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin




import config
# DATABASE = SqliteDatabase('memes.sqlite')






class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password =  CharField()
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    # def get_memes(self):
    #     return Meme.select().where(
    #         (meme.created_by == self)
    #     )

    @classmethod
    def create_user(cls, username, email, password, is_admin):
        # removed .lower()
        email = email
        try:
            cls.select().where(
                (cls.email == email)
                ).get()
        except cls.DoesNotExist:
            user = cls(username = username, email = email, is_admin = is_admin)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else: 
            raise Exception('That email or password already exists')

class Meme(Model):
    image = CharField()
    top_text = CharField()
    bottom_text = CharField()
    votes = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)
    created_by = ForeignKeyField(User, backref='meme_user')

    class Meta():
        database = DATABASE
        db_table = 'memes'

    @classmethod
    def create_meme(cls, image, top_text, bottom_text, votes, created_by, created_at):
        meme = cls(image = image, top_text = top_text, bottom_text = bottom_text, votes = votes, created_at = created_at, created_by = created_by)
        meme.save()
        return meme
        


class Favs(Model):
    user_id = ForeignKeyField(User, backref='users')
    meme_id = ForeignKeyField(Meme, backref='memes')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Meme], safe=True)
    DATABASE.close()


