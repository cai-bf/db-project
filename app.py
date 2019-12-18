# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import redis

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
app.redis = r

from middleware.auth import *


from controller.auth import auth
app.register_blueprint(auth)
from controller.user import user_bp
app.register_blueprint(user_bp)
from controller.goods import goods_bp
app.register_blueprint(goods_bp)
from controller.attachment import attach_bp
app.register_blueprint(attach_bp)
from controller.address import addr_bp
app.register_blueprint(addr_bp)
from controller.category import category_bp
app.register_blueprint(category_bp)
from controller.order import order_bp
app.register_blueprint(order_bp)
from controller.comment import comment_bp
app.register_blueprint(comment_bp)


# 引入models
from model.user import User
from model.goods import Goods
from model.order import Order
from model.comment import Comment
from model.address import Address
from model.item import Item
from model.category import Category


if __name__ == '__main__':
    app.run('127.0.0.1', 8888)
