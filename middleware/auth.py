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
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except:
            return {'errmsg': '未登录或已过期', 'errcode': 401}, 401
        g.current_user = User.query.get(user_id)
