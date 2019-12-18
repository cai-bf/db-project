# coding:utf-8
from flask import Blueprint, request, g, jsonify
from model.goods import Goods
from model.category import Category
from json import dumps
from app import db, app

goods_bp = Blueprint('goods_bp', __name__)


@goods_bp.route('/my_goods', methods=['GET'])
def get_goods():
    page = request.args.get('page', 1, type=int)
    user = g.current_user
    res = user.get_goods(page)
    return {
       'items': [val.to_dict() for val in res.items],
       'has_next': res.has_next,
       'has_prev': res.has_prev,
       'page': res.page,
       'pages': res.pages,
       'per_page': res.per_page,
       'prev_num': res.prev_num,
       'next_num': res.next_num,
       'total': res.total
    }, 200


@goods_bp.route('/my_goods', methods=['POST'])
def post_goods():
    user = g.current_user
    data = request.get_json()
    try:
        images = data['imgs']
        images = list(map(lambda x: app.config['IMG_BASE_URL'] + x, images))
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


@goods_bp.route('/goods/<int:id>', methods=['PUT'])
def edit_goods(id):
    user = g.current_user
    goods = user.goods.filter_by(sale=0, id=id).first()
    if goods is None:
        return {'errmsg': '没有权限修改该商品', 'errcode': 400}, 400
    data = request.get_json()
    try:
        if data.get('category_id') is not None:
            category = Category.query.filter_by(id=data['category_id']).first()
            if category is None:
                raise Exception
            goods.category_id = category.id
        if data.get('name') is not None:
            goods.name = data['name']
        if data.get('detail') is not None:
            goods.detail = data['detail']
        if data.get('price') is not None:
            goods.price = data['price']
        if data.get('imgs') is not None:
            images = data['imgs']
            images = list(map(lambda x: app.config['IMG_BASE_URL'] + x, images))
            goods.img = images[0]
            goods.imgs = dumps(images)
        db.session.commit()
        return {'errmsg': '修改成功', 'errcode': 200}, 200
    except:
        return {'errmsg': '数据出错, 请重新确认', 'errcode': 400}, 400


@goods_bp.route('/goods/search', methods=['GET'])
def search():
    page = request.args.get('page', 1, type=int)
    key = request.args.get('s')
    if key is None:
        return {'errmsg': '请输入搜索关键词', 'errcode': 400}, 400
    goods = Goods.query.filter_by(sale=0).filter(Goods.name.like("%%%s%%" % key)) \
        .order_by(Goods.view.desc()).paginate(page, per_page=15, error_out=False)
    return {
           'items': [val.to_dict() for val in goods.items],
           'has_next': goods.has_next,
           'has_prev': goods.has_prev,
           'page': goods.page,
           'pages': goods.pages,
           'per_page': goods.per_page,
           'prev_num': goods.prev_num,
           'next_num': goods.next_num,
           'total': goods.total
       }, 200


@goods_bp.route('/goods/<int:id>', methods=['DELETE'])
def del_goods(id):
    user = g.current_user
    goods = user.goods.filter_by(id=id).first()
    if goods is None:
        return {'errmsg': '没有权限删除商品', 'errcode': 400}, 400
    if goods.sale == 1:
        return {'errmsg': '已售出商品不可删除', 'errcode': 400}, 400
    db.session.delete(goods)
    return {'errmsg': '删除成功', 'errcode': 200}, 200


@goods_bp.route('/goods/index')
def index():
    category_id = request.args.get('category_id', 0, type=int)
    if category_id == 0:
        data = Goods.query.order_by(Goods.view.desc()).limit(30).all()
    else:
        category = Category.query.filter_by(id=category_id).first()
        if category is None:
            return {'errmsg': '分类信息出错', 'errcode': 400}, 400
        data = Goods.query.filter_by(category_id=category_id).order_by(Goods.view.desc()).limit(30).all()
    return jsonify([val.to_dict() for val in data]), 200


@goods_bp.route('/goods/view')
def incr_view():
    id = request.args['id']
    Goods.query.filter_by(id=id).update({'view': Goods.view + 1})
    db.session.commit()
    return "", 204
