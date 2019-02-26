import datetime

from peewee import *

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin



DATABASE = SqliteDatabase('memes.sqlite')


class Meme(Model):
    image = CharField()
    top_text = CharField()
    bottom_text = CharField()
    votes = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta():
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Meme], safe=True)
    DATABASE.close()


