# -*- coding: utf-8 -*-
# FileName  : views.py
# Author    : shiqianlong

from flask import Blueprint, send_from_directory, current_app

bp = Blueprint('media', __name__, url_prefix='/media')


@bp.route('/avatars/<filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)
