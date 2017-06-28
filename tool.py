# -*- coding: utf-8 -*-

import os
import chardet
import pymysql as pm

host = 'localhost'
user = 'root'
password = 'xmr123'
database = 'sampdb'

trainer_img = 'trainer_img'
trainer_info = 'trainer_info'
reco_img = 'reco_img'
reco_info = 'reco_info'

class SQLObject(object):
    '''
    需要启动mysql的服务端才能连接成功
    '''
    def __init__(self):
        pass
    # 执行多条语句
    @staticmethod
    def execute_sqls(sqls):
        db = pm.connect(host, user, password, database)
        try:
            with db.cursor() as cs:
                for sql in sqls:
                    cs.execute(sql)
            db.commit()
        finally:
            db.close()
    @staticmethod
    def execute_sql(sql):
        db = pm.connect(host, user, password, database)
        try:
            with db.cursor() as cs:
                cs.execute(sql)
            db.commit()
        finally:
            db.close()

    @staticmethod
    def select_sql(sql):
        db = pm.connect(host, user, password, database)
        result = list()
        try:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()
                result = cs.fetchall()
        finally:
            db.close()
        return result

def make_dir(dir_path):
    if os.path.exists(dir_path):
        return False
    else:
        os.makedirs(dir_path)
    return True


def make_file(filepath):
    thedir, filename = os.path.split(filepath)
    if not thedir or not filename:
        return False

    if not os.path.exists(filepath):
        make_dir(thedir)
        fh = open(filepath, 'w')
        fh.close()
        return True
    else:
        return False


def get_filename_from_dir(dir_path):
    if not os.path.exists(dir_path):
        return []

    filelist = []
    for item in os.listdir(dir_path):
        basename = os.path.basename(item)
        # print chardet.detect(basename)   # 找出文件名编码,文件名包含有中文

        # windows下文件编码为gb2312，linux下为utf-8
        try:
            decode_str = basename.decode("gb2312")
        except UnicodeDecodeError:
            decode_str = basename.decode("utf-8")

        filelist.append(decode_str)

    return filelist

def delete_session_dir():
    import shutil
    session_dir_path = './flask_session'
    try:
        if os.path.exists(session_dir_path):
            shutil.rmtree(session_dir_path)
    except:
        pass

if __name__ == '__main__':
    print make_file('./test/test/test.txt')
    print make_dir('./test/test/test')
