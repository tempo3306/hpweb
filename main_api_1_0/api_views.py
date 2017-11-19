# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2017/11/18 18:09
'''
from . import main_api
from flask import jsonify,request
import sqlalchemy
from ..models import User, Role, Permission, Auction, Action

@main_api.route('/userconfirm/info',methods=['GET'])
def userconfirm():
    print("fdsf")
    username=request.args.get('username')
    passwd=request.args.get('passwd')
    user=User.query.filter_by(username=username).first()  #判断用户是否存在
    if user:
        result=user.verify_password(passwd)
        if result:
            return jsonify({'result':'success',
                            'url_dianxin':'www.baidu.com',
                            'url_nodianxin':'www.qq.com'})
        else:
            return jsonify({'result':'failure'})
    else:
        return jsonify({'result': 'failure'})