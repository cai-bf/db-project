# coding:utf-8
from app import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'goods_id': self.goods_id,
            'goods': self.goods.to_dict()
        }
