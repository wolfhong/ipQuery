#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
import socket
from multiprocessing import Process, Lock

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import requests
from ormapp.models import Block, Location

lock = Lock()


def _ip_to_int(ip_str):
    regular = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)')
    match = regular.match(ip_str)
    if not match:
        raise ValueError('IP format error')
    v1, v2, v3, v4 = match.groups()
    v1, v2, v3, v4 = int(v1), int(v2), int(v3), int(v4)
    return v1 * 256 ** 3 + v2 * 256 ** 2 + v3 * 256 + v4


def query_db(ip_str):
    ip = _ip_to_int(ip_str)  # change into int
    block_list = Block.objects.filter(start_ip_num__lte=ip, end_ip_num__gte=ip)
    for block in block_list:
        loc = Location.objects.filter(id=block.loc_id).first()
        if loc:
            lock.acquire()
            sys.stdout.write('GeoIp: ')
            print(loc)
            lock.release()


def query_chinaz(ip_str):
    loc = None
    try:
        url = 'http://ip.chinaz.com/ajaxsync.aspx?at=ipbatch&callback=jq&jdfwkey=oymcy2&ip=%s' % ip_str
        r = requests.post(url, timeout=3)
        left = r.text.index("location:'")
        if left > 0:
            left += len("location:'")
            right = r.text[left:].index("'")
            if right > 0:
                loc = r.text[left:left+right]
    except:
        pass
    if loc:
        lock.acquire()
        print(loc)
        lock.release()


def main():
    ip_str = socket.gethostbyname(sys.argv[1])
    print('ip: %s' % ip_str)
    p_list = []
    p_list.append(Process(target=query_db, args=(ip_str, )))
    p_list.append(Process(target=query_chinaz, args=(ip_str, )))
    [p.start() for p in p_list]
    [p.join() for p in p_list]


if __name__ == '__main__':
    main()
