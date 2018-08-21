# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .utils import code2_to_name, PY3

'''
Blocks:
    startIpNum,endIpNum,locId
Location:
    locId,country,region,city,postalCode,latitude,longitude,metroCode,areaCode
'''


class Block(models.Model):
    id = models.AutoField(primary_key=True)
    start_ip_num = models.IntegerField(db_index=True)
    end_ip_num = models.IntegerField(db_index=True)
    loc_id = models.IntegerField(db_index=True)


class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=10)
    region = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    metro_code = models.CharField(max_length=10)
    area_code = models.CharField(max_length=10)

    def __unicode__(self):
        zh_name = code2_to_name.get(self.country, '')
        if zh_name:
            zh_name = '(%s)' % zh_name
        return "country=%s%s | region=%s | city=%s | longitude=%s | latitude=%s" % \
                (self.country, zh_name, self.region, self.city, self.longitude, self.latitude)

if PY3:
    setattr(Location, '__str__', Location.__unicode__)
    delattr(Location, '__unicode__')
