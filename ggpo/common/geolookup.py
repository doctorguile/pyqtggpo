# -*- coding: utf-8 -*-
import json
import os
import urllib2
from ggpo.common.runtime import *
from ggpo.common.settings import Settings
from ggpo.common.util import packagePathJoin


def findGeoIPDB():
    dbs = [Settings.value(Settings.GEOIP2DB_LOCATION),
           os.path.join(os.getcwd(), 'GeoLite2-City.mmdb'),
           packagePathJoin('GeoLite2-City.mmdb'),
           os.path.join(os.getcwd(), 'GeoLite2-Country.mmdb'),
           packagePathJoin('GeoLite2-Country.mmdb')]
    for db in dbs:
        if db and os.path.isfile(db):
            return db


def freegeoip(ip):
    url = 'http://freegeoip.net/json/'
    try:
        response = urllib2.urlopen(url + ip, timeout=1).read().strip()
        return json.loads(response)
    except urllib2.URLError:
        return {'areacode': '',
                'city': '',
                'country_code': '',
                'country_name': '',
                'ip': ip,
                'latitude': '',
                'longitude': '',
                'metro_code': '',
                'region_code': '',
                'region_name': '',
                'zipcode': ''}

_geoIP2Reader = False


def geolookup(ip):
    if not _geoIP2Reader:
        geolookupInit()
    if _geoIP2Reader:
        # noinspection PyBroadException
        try:
            response = _geoIP2Reader.city(ip)
            cc = response.country.iso_code.lower()
            return cc, response.country.name, response.city.name
        except:
            pass
    return 'unknown', '', ''


def geolookupInit():
    global _geoIP2Reader
    db = findGeoIPDB()
    if db and os.path.isfile(db):
        _geoIP2Reader = GeoIP2Reader(db)


def isUnknownCountryCode(cc):
    return not cc or cc == 'unknown'
