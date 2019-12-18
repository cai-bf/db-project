# coding:utf-8
from flask import Blueprint, g, request
from model.user import User
from app import db


user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/user", methods=['GET'])
def get_user():
    user = g.current_user
    return user.to_dict(), 200


@user_bp.route('/user', methods=['PUT'])
def update_user():
    user = g.current_user
    data = request.get_json()
    if data.get('password') is not None and data['password'].strip() != '':
        if data.get('old_password') is None or user.check_password(data.get('old_password')) is False:
            return {'errmsg': '原密码错误', 'errcode': 400}, 400
        user.password = User.generate_password(data['password'])
    if data.get('name') is not None and data['name'].strip() != '':
        user.name = data['name']
    db.session.commit()
    return {'errmsg': '修改成功', 'errcode': 200}, 200
