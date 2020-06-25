import datetime
from mongoengine import CASCADE
from wtforms.validators import EqualTo, Length

from application.mongodb import db


class Users(db.Document):
    user_id = db.StringField()
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True, validators=[Length(min=8, max=20)])
    confirm = db.StringField(required=True, validators=[EqualTo('password', message='Passwords must match')])
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)


class AuthClients(db.Document):
    name = db.StringField(required=True)
    secret = db.StringField(required=True)
    redirect_url = db.StringField()
    user_id = db.ReferenceField(Users, reverse_delete_rule=CASCADE)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)


class AuthAccessTokens(db.Document):
    access_token = db.StringField(required=True)
    client_id = db.ReferenceField(AuthClients, reverse_delete_rule=CASCADE)
    user_id = db.ReferenceField(Users, reverse_delete_rule=CASCADE)
    expired_at = db.DateTimeField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    revoked = db.IntField(default=None)


class AuthRefreshTokens(db.Document):
    access_token_id = db.ReferenceField(AuthAccessTokens, reverse_delete_rule=CASCADE)
    refresh_token = db.StringField(required=True)
    user_id = db.ReferenceField(Users, reverse_delete_rule=CASCADE)
    client_id = db.ReferenceField(AuthClients, reverse_delete_rule=CASCADE)
    expired_at = db.DateTimeField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    revoked = db.IntField(default=None)