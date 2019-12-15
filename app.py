# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

from middleware.auth import *


from controller.auth import auth
app.register_blueprint(auth)
from controller.user import user_bp
app.register_blueprint(user_bp)
from controller.goods import goods_bp
app.register_blueprint(goods_bp)
from controller.attachment import attach_bp
app.register_blueprint(attach_bp)

# 引入models
from model.user import User
from model.goods import Goods
from model.order import Order
from model.comment import Comment
from model.address import Address
from model.item import Item


if __name__ == '__main__':
    app.run('127.0.0.1', 8888)
