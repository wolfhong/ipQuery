# -*- coding: utf-8 -*-
import sys
import os
import csv
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from ormapp.models import Block, Location

'''
samples数据下载地址: https://dev.maxmind.com/geoip/legacy/geolite/
执行前, GeoLiteCity-Location.csv使用sublime工具Save with Encoding -> UTF8
'''

PY3 = sys.version_info[0] == 3


def read_csv(filename, count):
    # 从网络下载的原始数据,前两行是无效的
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        index = 0
        for row in spamreader:
            index += 1
            if index <= 2:
                continue
            if len(row) == count:
                yield row


def to_unicode(s):
    if PY3:
        return s.decode('utf8', 'replace') if isinstance(s, bytes) else s
    else:
        return s.decode('utf8', 'replace') if isinstance(s, str) else s


def write_into_block():
    # 写入Block数据
    obj_list = []
    LIMIT = 1000
    for row in read_csv('./samples/GeoLiteCity-Blocks.csv', 3):
        obj = Block()
        obj.start_ip_num = int(row[0])
        obj.end_ip_num = int(row[1])
        obj.loc_id = int(row[2])

        obj_list.append(obj)
        if len(obj_list) >= LIMIT:
            Block.objects.bulk_create(obj_list)
            obj_list = []
    if obj_list:
        Block.objects.bulk_create(obj_list)
        obj_list = []


def write_into_loc():
    # 写入Location数据
    obj_list = []
    LIMIT = 1000
    for row in read_csv('./samples/GeoLiteCity-Location.csv', 9):
        obj = Location()
        obj.id = int(row[0])
        obj.country = to_unicode(row[1])
        obj.region = to_unicode(row[2])
        obj.city = to_unicode(row[3])
        obj.postal_code = to_unicode(row[4])
        obj.latitude = to_unicode(row[5])
        obj.longitude = to_unicode(row[6])
        obj.metro_code = to_unicode(row[7])
        obj.area_code = to_unicode(row[8])

        obj_list.append(obj)
        if len(obj_list) >= LIMIT:
            Location.objects.bulk_create(obj_list)
            obj_list = []
    if obj_list:
        Location.objects.bulk_create(obj_list)
        obj_list = []


if __name__ == '__main__':
    ''' 将GeoIp数据写入数据库 '''
    write_into_block()
    write_into_loc()
