# -*- coding:utf-8 -*-

car_info_log = './static/Recoraw/20170414.log'
import time
import random

count = 0
while 1:
    time.sleep(0.3)
    count += random.randint(1, 3)
    f = open(car_info_log, 'a')
    timestr = str(time.time())
    speed = str(random.randint(50, 150) + random.randint(50, 150)/7.0)
    countstr = str(count)
    line = timestr + ',' + speed + ',' + countstr + ',\n'
    f.writelines([line])
    f.close()