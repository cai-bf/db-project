# coding:utf-8
from app import db
import datetime
from json import loads


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(150))
    price = db.Column(db.Float(2), default=0)
    sale = db.Column(db.Integer, default=0)
    # stock = db.Column(db.Integer, default=1)
    view = db.Column(db.Integer, comment="浏览次数", default=0)
    img = db.Column(db.String(255), nullable=False)
    imgs = db.Column(db.Text, nullable=False)
    # state = db.Column(TINYINT(), comment="审核状态, 0待审核, 1审核通过, 2不通过", default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    item = db.relationship('Item', backref='goods', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'vendor': self.vendor.to_dict(),
            'name': self.name,
            'detail': self.detail,
            'price': self.price,
            'sale': self.sale,
            # 'stock': self.stock,
            'view': self.view,
            'img': self.img,
            'imgs': loads(self.imgs),
            'category_id': self.category_id,
            'category': self.category.to_dict(),
            # 'state': self.state,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
