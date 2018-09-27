# -*- coding: utf-8 -*-
from flask_login import UserMixin
from exts import login_manger
from exts import db


class Role(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(64), index=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


# class User(UserMixin, db.Model):
#     ###User继承UserMixin和db.Model类的功能属性
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(64), unique=True, index=True)
#     password = db.Column(db.String, nullable=False)


class Cpu_status(db.Model):
    __tablename__ = 'cpu_used'
    id = db.Column(db.Integer, primary_key=True)
    add_time = db.Column(db.String, nullable=False)
    cpu_used = db.Column(db.String, nullable=False)


@login_manger.user_loader
def load_user(user_id):
    return Role.query.get(int(user_id))
