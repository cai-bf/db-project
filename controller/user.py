# coding:utf-8
from flask import Blueprint, g


user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/user", methods=['GET'])
def get_user():
    user = g.current_user
    return user.to_dict(), 200
