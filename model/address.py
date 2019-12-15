# coding:utf-8
from datetime import datetime

from app import db


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    county = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    orders = db.relationship('Order', backref='address', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'phone': self.phone,
            'province': self.province,
            'city': self.city,
            'county': self.county,
            'detail': self.detail,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
