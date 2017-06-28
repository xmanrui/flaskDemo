# -*- coding: utf-8 -*-

import os
from tool import SQLObject
import tool

trainerimagepath = './static/trainer'
recoimagepath = './static/recoraw'
logpath = './static/recoraw/20170417.log'
logdir = './static/recoraw'

def get_imgs(imgdir):
    result = dict()
    for name in os.listdir(imgdir):
        namepath = os.path.join(imgdir, name)
        if os.path.isdir(namepath):
            result[name] = list()
            for img in os.listdir(namepath):
                if os.path.isfile(os.path.join(namepath, img)) and img.endswith(('jpg', 'png')):
                    result[name].append(img)

    return result

def get_trainer_img(imgdir):
    result = get_imgs(imgdir)
    return result


def get_reco_img(imgdir):
    result = get_imgs(imgdir)
    return result

def joint_sql_update_img_table(table, namevalue, imgvalue):
    # ignore : 记录存在则不插入，忽略掉
    sql = 'insert ignore into %s(name, img) values("%s", "%s")' % (table, namevalue, imgvalue)
    return sql

def joint_sql_update_trainer_img_table(namevalue, imgvalue):
    sql = joint_sql_update_img_table(tool.trainer_img, namevalue, imgvalue)
    return sql

def joint_sql_update_reco_img_table(namevalue, imgvalue):
    sql = joint_sql_update_img_table(tool.reco_img, namevalue, imgvalue)
    return sql

def joint_update_info_table(table, name, finddatetime, address, confidence, findtime, img, filename):
    # ignore : 记录存在则不插入，忽略掉
    sql = 'insert ignore into %s(name, finddatetime, address, confidence, findtime, img, filename) values("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (table, name, finddatetime, address, confidence, findtime, img, filename)
    return sql


def update_trainer_img_table():
    imgdict = get_trainer_img(trainerimagepath)
    sqls = list()
    for name, imgs in imgdict.items():
        for img in imgs:
            print img
            sql = joint_sql_update_trainer_img_table(name, img)
            sqls.append(sql)
    SQLObject.execute_sqls(sqls)


def update_reco_img_table():
    imgdict = get_reco_img(recoimagepath)
    sqls = list()
    for name, imgs in imgdict.items():
        for img in imgs:
            print img
            sql = joint_sql_update_reco_img_table(name, img)
            sqls.append(sql)
    SQLObject.execute_sqls(sqls)


def get_logfiles(log_dir):
    logfile = list()
    for item in os.listdir(log_dir):
        path = os.path.join(logdir, item)
        if os.path.isfile(logpath) and item.endswith('log'):
            logfile.append(path)

    return logfile

def convert_datetime(strdt):
    '''
    把strdt转化为 2017-04-20 14:20:36 这种形式的时间字符串
    '''
    # todo 完善年月日的转换
    Y_m_d = '2017-04-20'
    H_M_S = '00:00:00'
    result = ''
    if len(strdt) >= 6:
        H_M_S = ''.join((strdt[0:2], ':', strdt[2:4], ':', strdt[4:6]))

    result = Y_m_d + " " + H_M_S

    return result

def get_info(line):
    line = line.rstrip()
    line = line.rstrip(',')
    strsplit = line.split(',')
    data = dict()
    if len(strsplit) == 7:
        # todo: 把strsplit[1] 转化为2017-04-20 14:20:36 这种形式的时间字符串
        data['name'] = strsplit[0]
        data['finddatetime'] = convert_datetime(strsplit[1])
        data['address'] = strsplit[2]
        data['confidence'] = strsplit[3]
        data['findtime'] = '%.2f'% float(strsplit[4])
        #data[] = strsplit[5] # 第五项值暂时无意义
        data['img'] = strsplit[6]

    return data


def get_data_from_log(logpath):
    data = list()
    try:
        with open(logpath, 'r') as fh:
            lines = fh.readlines()
            for i in lines:
                filename = os.path.basename(logpath)
                info = get_info(i)
                info['filename'] = filename
                if info: data.append(info)
    except IOError:
        pass

    return data


def update_reco_info_table(logpath):
    data = get_data_from_log(logpath)
    sqls = list()
    for item in data:
        sql = joint_update_info_table(tool.reco_info, item['name'], item['finddatetime'], item['address'], item['confidence'], item['findtime'], item['img'], item['filename'])
        sqls.append(sql)
    SQLObject.execute_sqls(sqls)


def all_update_reco_info_table():
    logfiles = get_logfiles(logdir)
    for file in logfiles:
        update_reco_info_table(file)


def update_trainer_info_table():

    pass


if __name__ == '__main__':
    # update_trainer_img_table()
    # update_reco_img_table()
    all_update_reco_info_table()
