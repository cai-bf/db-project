# coding:utf-8
from flask import request, g, Blueprint
from app import db
from model.comment import Comment


comment_bp = Blueprint('comment_bp', __name__)


@comment_bp.route('/comment', methods=['POST'])
def create_comment():
    user = g.current_user
    data = request.get_json()
    order = user.orders.filter_by(id=data['order_id']).first()
    if order is None:
        return {'errmsg': '无权执行操作', 'errcode': 400}, 400
    if order.state != '已确认收货':
        return {'errmsg': '确认收货后才可评论哦', 'errcode': 400}, 400
    if order.comment.first() is not None:
        return {'errmsg': '已经评论过了哦', 'errcode': 400}, 400
    comment = Comment(order=order, user=user, content=data['content'])
    db.session.add(comment)
    db.session.commit()
    return {'errmsg': '发表评论成功', 'errcode': 200}, 200
