# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

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
        return "country=%s | region=%s | city=%s | longitude=%s | latitude=%s" % (self.country, self.region, self.city, self.longitude, self.latitude)

    def __str__(self):
        return self.__unicode__()
