# encoding: utf-8
'''
@author: zhushen
@contact: 810909753@q.com
@time: 2017/9/10 12:06
'''

import datetime
import datetime
s="2017/07/01"
format = '%Y/%m/%d'
dt=datetime.datetime.strptime(s,format).date()
print(dt)

# date_str="2017/07/01"
# data = datetime.datetime.strptime(date_str, format='%Y/%m/%d').date()
