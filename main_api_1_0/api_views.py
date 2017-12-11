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
    import time
    time1 = time.localtime(time.time())
    time2 = time.strftime("%Y%m%d", time1)
    today_date = "time2" + "01"
    url_dianxin = "https://paimai2.alltobid.com/bid/%s/login.htm" % today_date
    url_nodianxin = "https://paimai.alltobid.com/bid/%s/login.htm" % today_date

    # url_dianxin = "https://paimai2.alltobid.com/bid/%s/login.htm" % today_date
    # url_nodianxin = "https://paimai.alltobid.com/bid/%s/login.htm" % today_date

    username=request.args.get('username')
    passwd=request.args.get('passwd')
    user=User.query.filter_by(username=username).first()  #判断用户是否存在
    if user:
        result=user.verify_password(passwd)
        if result:
            return jsonify({'result':'login success',
                            'url_dianxin':url_dianxin,
                            'url_nodianxin':url_nodianxin})
        else:
            return jsonify({'result':'wrong password'})
    else:
        return jsonify({'result': 'wrong account'})