# -*- coding: utf-8 -*-

import logging
import tool
import threading
from read_setting_conf import ReadSettingConf

Lock = threading.Lock()


class SettingLogSingleton(object):
    '''
    log只能初始化一次，否则写log会重复，所以才使用单例模式
    '''
    # 定义静态变量实例
    __instance = None

    def __init__(self):
        pass

    @staticmethod
    def add_message_to_setting_log(msg):
        read_obj = ReadSettingConf()
        setting_log_filename = read_obj.get_log_filename()
        logger = logging.getLogger(setting_log_filename)
        logger.debug(msg)

    @staticmethod
    def __init_logger():
        read_obj = ReadSettingConf()
        setting_log_filename = read_obj.get_log_filename()
        tool.make_file(setting_log_filename)
        logger = logging.getLogger(setting_log_filename)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(setting_log_filename)
        fh.setLevel(logging.DEBUG)
        fm = 'setting_log: %(levelname)s: [%(filename)s line:%(lineno)d %(funcName)s] -- [%(asctime)s]  %(message)s'
        formatter = logging.Formatter(fm)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                # double check
                if not cls.__instance:
                    # cls.__instance = super(SettingLogSingleton, cls).__new__(cls, *args, **kwargs)
                    cls.__instance = object.__new__(cls, *args)
                    cls.__instance.__init_logger()
            finally:
                Lock.release()
        return cls.__instance


def test_singleton():
    obj2 = SettingLogSingleton()
    obj = SettingLogSingleton()
    print id(obj)
    obj.add_message_to_setting_log('*' * 80)
    obj = SettingLogSingleton()
    print id(obj)
    obj.add_message_to_setting_log('for testing')
    obj = SettingLogSingleton()
    obj.add_message_to_setting_log('for testing')
    obj.add_message_to_setting_log('for testing')
    print id(obj)

if __name__ == "__main__":
    test_singleton()



