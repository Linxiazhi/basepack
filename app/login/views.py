# -*-coding: utf-8-*-
from . import login
from flask import jsonify, request
from app.models import db, User
from app.util.get_request_param import get_form_param
from app.util.custom_error import CustomFlaskErr
import logging
import traceback


# 登陆
@login.route('/login', methods=('GET', 'POST'))
def synchronous_resource():
    try:
        phone = get_form_param('Phone', type='int' ,not_none=True)
        password = get_form_param('Password', not_none=True)
        user = User.query.filter(User.phone == phone).first()
        if user is not None:
            login_user(user)
            # 写入最后登录时间
            user.lastloginTime = int(time.time())
            user.lastloginIP = request.remote_addr
            db.session.add(user)
            db.session.commit()
            return jsonify({'Code': 'Success', 'Message': 'Success'})
        else:
            pass
    except Exception as e:
        traceback.print_exc()
        logging.error('synchronous resource failed. %s' % e.message)
        raise CustomFlaskErr('UnknownError')