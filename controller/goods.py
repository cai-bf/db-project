# coding:utf-8
from flask import Blueprint, request, g, jsonify
from model.goods import Goods
from json import dumps
from app import db, app


goods_bp = Blueprint('goods_bp', __name__)


@goods_bp.route('/my_goods', methods=['GET'])
def get_goods():
    user = g.current_user
    res = user.get_goods()
    return jsonify([r.to_dict() for r in res]), 200


@goods_bp.route('/my_goods', methods=['POST'])
def post_goods():
    user = g.current_user
    data = request.get_json()
    images = data['imgs']
    images = list(map(lambda x: app.config['IMG_BASE_URL'] + x, images))

    goods = Goods(vendor=user, name=data['name'], detail=data.get('detail'), price=data['price'], stock=data['stock'],
                  img=images[0], imgs=dumps(images))
    db.session.add(goods)
    db.session.commit()
    return {'errmsg': '发布商品成功', 'errcode': 200}, 200

