# -*- coding: utf-8 -*-
# FileName  : views.py
# Author    : shiqianlong
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils import restful

bp = Blueprint('cmsapi', __name__, url_prefix='/cmsapi')


@bp.route('/')
@jwt_required()
def mytest():
    identity = get_jwt_identity()
    return restful.ok(data={'identity': identity}, message='success')
