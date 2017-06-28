# -*- coding: utf-8 -*-

import ConfigParser


class ReadSettingConf:

    def __init__(self):
        conf_path = './config/setting.conf'
        cf = ConfigParser.ConfigParser()
        cf.read(conf_path)
        self.__log_dir = cf.get('setting', 'setting_log_dir')
        self.__log_filename = cf.get('setting', 'setting_log_filename')

    def get_log_dir(self):
        return self.__log_dir

    def get_log_filename(self):
        return self.__log_filename


if __name__ == "__main__":
    obj = ReadSettingConf()
    print obj.get_log_dir()
    print obj.get_log_filename()
