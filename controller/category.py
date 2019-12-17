# coding:utf-8
from flask import Blueprint, jsonify
from model.category import Category


category_bp = Blueprint('category_bp', __name__)


@category_bp.route('/categories')
def get_categories():
    data = Category.query.all()
    return jsonify([val.to_dict() for val in data]), 200
