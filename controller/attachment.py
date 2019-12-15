# coding:utf-8
from flask import request, Blueprint, jsonify
import uuid
import os
from app import app


attach_bp = Blueprint('attach_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@attach_bp.route('/upload', methods=['POST'])
def upload():
    names = []
    for file in request.files.values():
        if file and allowed_file(file.filename):
            filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            names.append(filename)
    return jsonify(names), 200
