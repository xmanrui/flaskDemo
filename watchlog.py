# -*- coding: utf-8 -*-

from watchdog.observers import Observer
from watchdog.events import *
import time
from read_setting_conf import ReadSettingConf
import tool
import os


class LogFileEventHandler(FileSystemEventHandler):
    def __init__(self, log_filename):
        FileSystemEventHandler.__init__(self)
        self.log_filename = log_filename
        texts = self.read_log_file()
        self.lineNum = len(texts)

    def read_log_file(self):
        fhandle = open(self.log_filename, 'r')
        try:
            all_the_text = fhandle.readlines()
        except IOError:
            all_the_text = []
        finally:
            fhandle.close()

        return all_the_text

    def on_modified(self, event):
        '''
        一次修改log_filename文件会调用三次on_modified，每次的event.src_path都不一样，类似:
        ./log\mylog.log___jb_tmp___
        ./log\mylog.log___jb_old___
        ./log\mylog.log
        前两次会加上后缀，此时mylog.log不可访问，第三次才可以，所以要判断event.src_path和self.log_filename，
        不相等则退出本函数。
        '''

        if os.path.abspath(event.src_path) != os.path.abspath(self.log_filename):
            return
        all_the_text = self.read_log_file()
        lineNum = len(all_the_text)
        if lineNum != self.lineNum:
            offset = lineNum - self.lineNum
            if offset > 0:
                for i in range(offset):
                    print all_the_text[self.lineNum + i].rstrip('\n')
            self.lineNum = lineNum

        print '*' * 80

if __name__ == "__main__":
    read_obj = ReadSettingConf()
    setting_log_dir = read_obj.get_log_dir()
    setting_log_filename = read_obj.get_log_filename()
    tool.make_file(setting_log_filename)
    observer = Observer()
    event_handler = LogFileEventHandler(setting_log_filename)
    observer.schedule(event_handler, setting_log_dir, True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
