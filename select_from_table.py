# -*- coding: utf-8 -*-

from tool import SQLObject


def select_data_by_filename(table, name, filename):
    sql = 'select * from %s where name = "%s" and filename = "%s"' % (table, name, filename)
    result = SQLObject.select_sql(sql)
    return result


def select_data_by_address(table, name, address):
    sql = 'select * from %s where name ="%s" and address = "%s" ' % (table, name, address)
    result = SQLObject.select_sql(sql)
    return result


def select_img_by_name(table, name):
    sql = 'select img from %s where name = "%s"' % (table, name)
    result = SQLObject.select_sql(sql)
    return result


def test_select_data():
    table_info = 'reco_info'
    table_img = 'trainer_img'
    name = '130'
    filename = '20170417.log'
    address = '1003'
    r1 = select_data_by_filename(table_info, name, filename)
    r2 = select_data_by_address(table_info, name, address)
    r3 = select_img_by_name(table_img, name)
    print r3


if __name__ == '__main__':
    test_select_data()
