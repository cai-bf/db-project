# coding:utf-8
from flask import Blueprint, request, g, jsonify
from model.goods import Goods
from model.category import Category
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
    try:
        category = Category.query.filter_by(id=data['category_id']).first()
        if category is None:
            raise Exception
        goods = Goods(vendor=user, name=data['name'], detail=data.get('detail'), price=data['price'],
                  img=images[0], imgs=dumps(images), category=category)
        db.session.add(goods)
        db.session.commit()
    except:
        return {'errmsg': '数据出错, 请重新确认', 'errcode': 400}, 400
    return {'errmsg': '发布商品成功', 'errcode': 200}, 200

