# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2017/11/18 18:01
'''

from flask import Blueprint

main_api=Blueprint('main_api',__name__)

from . import api_views
from ..models import Permission


#app_context_processor flask的上下文处理器
# 1、app_context_processor作为一个装饰器修饰一个函数。
# 2、函数的返回结果必须是dict，届时dict中的key将作为变量在所有模板中可见。
#         定义了上述变量Permission中之后，我们直接在html模板中进行使用：
@main_api.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
