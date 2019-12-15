# coding:utf-8
from app import app
from flask import request, g
import jwt
from model.user import User


@app.before_request
def auth():
    token = request.headers.get('Authorization')
    path = request.path
    if path == '/login' or path == '/register':
        pass
        # next
    else:
        if token is None:
            return {'errmsg': '未登录或已过期', 'errcode': 401}, 401
        user_id = app.redis.get(token)
        if user_id is None:
            return {'errmsg': '未登录或已过期', 'errcode': 401}, 401
        g.current_user = User.query.get(user_id)
