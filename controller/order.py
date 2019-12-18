# coding:utf-8
from app import db
from flask import g, request, Blueprint
from model.goods import Goods
from model.order import Order
from model.item import Item

order_bp = Blueprint('order_bp', __name__)


@order_bp.route('/orders', methods=['POST'])
def create_orders():
    user = g.current_user
    data = request.get_json()

    items = []
    goods = Goods.query.filter(Goods.id.in_(data['goods_id'])).all()
    owner_id = goods[0].user_id if len(goods) != 0 else None
    if owner_id is None:
        return {'errmsg': '请选择商品!', 'errcode': 400}, 400
    for res in goods:
        if res.user_id != owner_id:
            return {'errmsg': '一次只能提交同一商家的商品', 'errcode': 400}, 400
        if res.sale == 1:
            return {'errmsg': '商品 ' + res.name + ' 已被购买, 下次手快点哦', 'errcode': 400}, 400
        items.append(Item(goods_id=res.id))
    if owner_id == user.id:
        return {'errmsg': '不可购买自己发布的商品', 'errcode': 400}, 400

    try:
        address = user.addresses.filter_by(id=data['address_id']).first()
        order = Order(user=user, owner_id=owner_id, address=address)
        order.items = items
        # 更新goods为已售出
        for val in goods:
            val.sale = 1
        db.session.add(order)
        db.session.commit()
        return {'errmsg': '下单成功, 请期待您的宝贝~', 'errcode': 200}, 200
    except:
        return {'errmsg': '数据出错, 请确认数据'}


@order_bp.route('/sold/orders')
def get_sold():
    user = g.current_user
    page = request.args.get('page', 1, type=int)
    data = user.get_sold(page)
    return {
           'items': [val.to_dict() for val in data.items],
           'has_next': data.has_next,
           'has_prev': data.has_prev,
           'page': data.page,
           'pages': data.pages,
           'per_page': data.per_page,
           'prev_num': data.prev_num,
           'next_num': data.next_num,
           'total': data.total
       }, 200


@order_bp.route('/purchases')
def get_purchases():
    user = g.current_user
    page = request.args.get('page', 1, type=int)
    state = request.args.get('state', -1, int)
    STATE = {
        1: '待发货',
        2: '已发货'
    }
    if state == -1:
        return {'errmsg': '参数错误, 未选择state参数', 'errcode': 400}, 400
    data = user.get_orders(page, STATE[state])
    return {
           'items': [val.to_dict() for val in data.items],
           'has_next': data.has_next,
           'has_prev': data.has_prev,
           'page': data.page,
           'pages': data.pages,
           'per_page': data.per_page,
           'prev_num': data.prev_num,
           'next_num': data.next_num,
           'total': data.total
       }, 200


@order_bp.route('/order/<int:id>/state', methods=['PUT'])
def edit_state(id):
    user = g.current_user
    order = user.sold.filter_by(id=id).first()
    if order is None:
        return {'errmsg': '没有权限修改或参数错误', 'errcode': 400}, 400
    data = request.get_json()
    state = ''
    if data['state'] == 1:
        state = '待发货'
        if order.state == '已发货':
            return {'errmsg': '已发货商品无法修改状态为待发货', 'errcode': 400}, 400
    elif data['state'] == 2:
        state = '已发货'
    order.state = state
    db.session.commit()
    return {'errmsg': '修改状态成功', 'errcode': 200}, 200
