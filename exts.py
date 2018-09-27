# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
# 用户认证
login_manger = LoginManager()
