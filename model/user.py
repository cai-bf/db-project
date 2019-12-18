# coding:utf-8
import datetime
import random
import string
from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from model.goods import Goods
from model.order import Order


def rand_token_str(size=128):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(size))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    goods = db.relationship('Goods', backref='vendor', lazy='dynamic')

    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    orders = db.relationship('Order', foreign_keys='Order.user_id', backref='user', lazy='dynamic')  # 购买的订单

    sold = db.relationship('Order', foreign_keys='Order.owner_id', backref='owner', lazy='dynamic')  # 卖出的订单

    addresses = db.relationship('Address', backref='user', lazy='dynamic')

    @staticmethod
    def generate_password(pswd):
        return generate_password_hash(pswd)

    def check_password(self, pswd):
        return check_password_hash(self.password, pswd)

    def get_token(self, expires_on=7200):
        token = rand_token_str()
        app.redis.set(token, self.id, ex=expires_on)
        return token

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_goods(self, page, per_page=15):
        return self.goods.order_by(Goods.created_at.desc()).filter_by(sale=0).paginate(page, per_page, error_out=False)

    def get_sold(self, page, per_page=15):
        return self.sold.order_by(Order.created_at.desc()).paginate(page, per_page, error_out=False)

    def get_orders(self, page, state, per_page=15):
        return self.orders.order_by(Order.created_at.desc()).filter_by(state=state)\
            .paginate(page, per_page, error_out=False)
