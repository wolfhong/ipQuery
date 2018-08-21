# -*- coding: utf-8 -*-
import os
import sys
import csv
import json

PY3 = sys.version_info[0] == 3


def read_csv(filename, count):
    # 前1行是无效的
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


code2_to_name = {}
code3_to_name = {}
num3_to_name = {}
net_to_name = {}


def csv_to_data():
    # 写入Location数据
    filename = os.path.join(os.path.dirname(os.path.join(__file__)), 'Country2code.csv')
    for row in read_csv(filename, 5):
        name = to_unicode(row[0])
        code2 = to_unicode(row[1])
        code3 = to_unicode(row[2])
        num3 = to_unicode(row[3])
        net = to_unicode(row[4])
        if code2 and code2 != to_unicode("不适用"):
            code2_to_name[code2] = name
        if code3 and code3 != to_unicode("不适用"):
            code3_to_name[code3] = name
        if num3 and num3 != to_unicode("不适用"):
            num3_to_name[num3] = name
        if net and net != to_unicode("不适用"):
            net_to_name[net] = name
    # data = {}
    # data['code2_to_name'] = code2_to_name
    # data['code3_to_name'] = code3_to_name
    # data['num3_to_name'] = num3_to_name
    # data['net_to_name'] = net_to_name
    # with open('samples/Country2code.json', 'w') as f_write:
    #     f_write.write(json.dumps(data))
    # print(data)

csv_to_data()
