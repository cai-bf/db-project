# coding:utf-8
from flask import Blueprint, request
from app import db
from model.user import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {'errmsg': '用户名不存在或密码错误', 'errcode': 401}, 401
    if not user.check_password(password):
        return {'errmsg': '用户名不存在或密码错误', 'errcode': 401}, 401
    token = user.get_token(7200)
    return {'Authorization': token}, 200


@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    name = data['name']
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return {'errmsg': '该用户名已存在', 'errcode': '400'}, 400
    user = User(username=username, password=User.generate_password(password), name=name)
    db.session.add(user)
    db.session.commit()
    return {'errmsg': '注册成功', 'errcode': '200'}, 200
