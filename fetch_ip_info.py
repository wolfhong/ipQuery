#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import sys
import os
import socket
from multiprocessing import Process, Lock

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import requests
from bs4 import BeautifulSoup
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
            sys.stdout.write('GeoIP: ')
            print(loc)
            print('-' * 30)
            lock.release()


def query_chinaz(ip_str):
    loc = None
    url = 'http://ip.chinaz.com/ajaxsync.aspx?at=ipbatch&callback=jq&jdfwkey=oymcy2&ip=%s' % ip_str
    try:
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
        sys.stdout.write('ip.chinaz.com: ')
        print(loc)
        print('-' * 30)
        lock.release()


def query_ipip(ip_str):
    url = 'https://labs.ipip.net/location/ip?ip=%s' % ip_str
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'}
    try:
        r = requests.get(url, timeout=3)
        soup = BeautifulSoup(r.text)
        rows = soup.find_all('div', attrs={'class': 'row'})
        if len(rows) >= 3:
            geo = rows[1].get_text()
            infos = '/'.join([td.get_text() for td in rows[2].find_all('td')])
            lock.acquire()
            print(geo)
            print(infos)
            print('visit: %s' % url)
            print('-' * 30)
            lock.release()
    except:
        pass


def query_ip138(ip_str):
    url = 'http://www.ip138.com/ips1388.asp?ip=%s&action=2' % ip_str
    try:
        r = requests.get(url, timeout=3)
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text)
        first_li = soup.find_all('ul', attrs={'class': 'ul1'})[0].find('li')
        if first_li:
            infos = first_li.get_text().strip('本站数据：')
            lock.acquire()
            sys.stdout.write('www.ip138.com: ')
            print(infos)
            print('-' * 30)
            lock.release()
    except:
        pass


def main():
    ip_str = socket.gethostbyname(sys.argv[1])
    print('ip: %s' % ip_str)
    p_list = []
    p_list.append(Process(target=query_db, args=(ip_str, )))
    p_list.append(Process(target=query_chinaz, args=(ip_str, )))
    p_list.append(Process(target=query_ipip, args=(ip_str, )))
    p_list.append(Process(target=query_ip138, args=(ip_str, )))
    [p.start() for p in p_list]
    [p.join() for p in p_list]


if __name__ == '__main__':
    main()
