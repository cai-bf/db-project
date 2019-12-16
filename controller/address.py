# coding:utf-8
from flask import request, g, Blueprint, jsonify
from model.address import Address
from app import db


addr_bp = Blueprint('addr_bp', __name__)


@addr_bp.route('/addresses', methods=['GET'])
def get_addresses():
    user = g.current_user
    addresses = user.addresses
    return jsonify([addr.to_dict() for addr in addresses]), 200


@addr_bp.route('/address', methods=['POST'])
def create_address():
    user = g.current_user
    data = request.get_json()
    try:
        address = Address(user=user, name=data['name'], phone=data['phone'], province=data['province'],
                          city=data['city'], county=data['county'], detail=data['detail'], code=data['code'])
        db.session.add(address)
        db.session.commit()
    except:
        return {'errmsg': '数据出错, 请重新确认', 'errcode': 400}, 400
    return {'errmsg': '添加成功', 'errcode': 200}, 200


@addr_bp.route('/address/<int:id>', methods=['PUT'])
def edit_address(id):
    user = g.current_user
    address = user.addresses.filter_by(id=id).first()
    if address is None:
        return {'errmsg': '没有权限!', 'errcode': 403}, 403
    try:
        address.from_dict(request.get_json())
        db.session.commit()
    except:
        return {'errmsg': '数据出错, 请重新确认', 'errcode': 400}, 400
    return {'errmsg': '修改成功', 'errcode': 200}, 200


@addr_bp.route('/address/<int:id>', methods=['DELETE'])
def delete_address(id):
    user = g.current_user
    addr = user.addresses.filter_by(id=id).first()
    if addr is None:
        return {'errmsg': '没有权限', 'errcode': 403}, 403
    db.session.delete(addr)
    db.session.commit()
    return "", 204
