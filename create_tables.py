# -*- coding: utf-8 -*-

from tool import SQLObject
import tool


def create_info_table(table_name):
    sql = '''create table if not exists %s
            (
             id int unsigned not null auto_increment primary key,
            name varchar(40) not null,
            index(name),
            finddatetime datetime not null,
            address varchar(100) not null,
            confidence varchar(10) not null,
            findtime varchar(20) not null,
            img varchar(100) not null,
            filename varchar(100) not null,
            unique(name, confidence, findtime, img, filename)
            );''' % table_name

    SQLObject.execute_sql(sql)


def create_img_table(table_name):
    sql = '''create table if not exists %s
            (
            id int unsigned not null auto_increment primary key,
            name varchar(40) not null,
            img varchar(100) not null,
            unique(name, img)
            );''' % table_name

    SQLObject.execute_sql(sql)


def create_trainer_img_table():
    create_img_table(tool.trainer_img)


def create_reco_img_table():
    create_img_table(tool.reco_img)


def create_trainer_info_table():
    create_info_table(tool.trainer_info)


def create_reco_info_table():
    create_info_table(tool.reco_info)


if __name__ == '__main__':
    create_trainer_img_table()
    create_reco_img_table()
    create_trainer_info_table()
    create_reco_info_table()
