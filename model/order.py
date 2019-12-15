# coding:utf-8
from datetime import datetime

from app import db
import random
import string


def rand_digit_str(size=18):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(size))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.Column(db.String(18), default=rand_digit_str, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    state = db.Column(db.String(20), default='待发货', comment='订单状态')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    items = db.relationship('Item', backref='order', lazy='dynamic')

    comment = db.relationship('Comment', backref='goods', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'owner_id': self.owner_id,
            'address_id': self.address_id,
            'state': self.state,
            'address': self.address.to_dict(),
            'item': self.items.to_dict(),
            'comment': self.comment.to_dict() if self.comment else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
