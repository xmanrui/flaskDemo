# -*- coding:utf-8 -*-

import os, sys
import shutil, mmap
from UserDict import UserDict

class MyDict(UserDict):
    def __init__(self, data={}, **kw):
        UserDict.__init__(self)
        self.update(data)
        self.update(kw)

    def __add__(self, other):
        d = MyDict(self.data)
        d.update(other)
        return d

a = MyDict(x='xie')
b = MyDict(y='yang')

print a + b

import errno
try:
    fp = open('no.such.file')
except IOError, (error, msg):
    if error == errno.ENOENT:
        print 'no such file'
    elif error == errno.EPERM:
        print 'permission denied'
    else:
        print msg


import errno
try:
    fp = open('no.such.file')
except IOError, error:
    if error.errno == errno.ENOENT:
        print 'no such file'
    elif error.errno == errno.EPERM:
        print 'permission denied'
    else:
        print error


import errno
try:
    fp = open('no.such.file')
except IOError as error:
    if error.errno == errno.ENOENT:
        print('no such file')
    elif error.errno == errno.EPERM:
        print('permission denied')
    else:
        print(error)

import sys, getopt

sys.argv = ['generate_car_info_log.py', '--echo', '--printer', 'lp01', '-e', 'message']
opts, args = getopt.getopt(sys.argv[1:], 'e:p:', ['echo', 'printer='])
print opts, ':::', args
import getpass
p = getpass.getpass()
print p

import hashlib
m = hashlib.md5()
strmy = 'xiemanrui'
m.update(strmy.encode('utf-8'))
a = m.hexdigest()
print(a)

>>> import array
>>> a = array.array('i', [1, 2, 3, 4])
>>> a.tostring()
b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00'
>>>

>>> import array
>>> array.array('H', [1, 2, 3, 4]).tostring()
b'\x01\x00\x02\x00\x03\x00\x04\x00'
>>> array.array('b', [1, 2, 3, 4]).tostring()
b'\x01\x02\x03\x04'
>>> array.array('i', [1, 2, 3, 4]).tostring()
b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00'
>>>

>>> array.array('H', [1]).tostring()
b'\x01\x00'
>>>

>>> array.array('H', [1]).tostring()
b'\x00\x01'
>>>

import array

def is_little_endian():
    a = array.array('H', [1]).tostring()
    if a[0] == 1:
        return True
    else:
        return False

