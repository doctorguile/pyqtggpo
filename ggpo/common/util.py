# -*- coding: utf-8 -*-
import hashlib
import logging
import logging.handlers
import json
import os
import re
import urllib2
from PyQt4 import QtGui, QtCore
from ggpo.common.runtime import *
from ggpo.common.settings import Settings
from ggpo.common import copyright
from os.path import expanduser


def checkUpdate():
    versionurl = 'https://raw.github.com/doctorguile/pyqtggpo/master/VERSION'
    #noinspection PyBroadException
    try:
        response = urllib2.urlopen(versionurl, timeout=2)
        latestVersion = int(response.read().strip())
        return latestVersion > copyright.__version__
    except:
        pass


def findGeoIPDB():
    dbs = [Settings.value(Settings.GEOIP2DB_LOCATION),
           os.path.join(os.getcwd(), 'GeoLite2-City.mmdb'),
           packagePathJoin('GeoLite2-City.mmdb'),
           os.path.join(os.getcwd(), 'GeoLite2-Country.mmdb'),
           packagePathJoin('GeoLite2-Country.mmdb')]
    for db in dbs:
        if db and os.path.isfile(db):
            return db


def findUnsupportedGamesavesDir():
    d = Settings.value(Settings.UNSUPPORTED_GAMESAVES_DIR)
    if d and os.path.isdir(d):
        return d
    d = os.path.abspath(os.path.join(expanduser("~"), "ggpoUnsupportedGamesavestates"))
    if d and os.path.isdir(d):
        return d
    # noinspection PyBroadException
    try:
        os.makedirs(d)
        return d
    except:
        pass


def findURLs(url):
    return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)


def findWine():
    if IS_WINDOWS:
        return True
    saved = Settings.value(Settings.WINE_LOCATION)
    if saved and os.path.isfile(saved):
        return saved
    w = None
    if IS_LINUX:
        w = '/usr/bin/wine'
    elif IS_OSX:
        w = '/Applications/Wine.app/Contents/Resources/bin/wine'
    if w and os.path.isfile(w):
        return w


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


def geolookup(ip):
    db = findGeoIPDB()
    if not GeoIP2Reader or not db:
        return 'unknown', '', ''
    # noinspection PyBroadException
    try:
        reader = GeoIP2Reader(db)
        response = reader.city(ip)
        cc = response.country.iso_code.lower()
        print cc, response.country.name, response.city.name
        return cc, response.country.name, response.city.name
    except:
        return 'unknown', '', ''


def isUnknownCountryCode(cc):
    return not cc or cc == 'unknown'


_loggerInitialzed = False


def logger():
    global _loggerInitialzed
    if not _loggerInitialzed:
        _loggerInitialzed = True
        return loggerInit()
    return logging.getLogger('GGPO')


def loggerInit():
    _logger = logging.getLogger('GGPO')
    _logger.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler(
        os.path.join(expanduser("~"), 'ggpo.log'), mode='a', maxBytes=100000, backupCount=4)
    if Settings.value(Settings.DEBUG_LOG):
        fh.setLevel(logging.INFO)
    else:
        fh.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    _logger.addHandler(fh)
    _logger.addHandler(ch)
    return _logger


def openURL(url):
    # noinspection PyCallByClass
    QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))


def packagePathJoin(*args):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, *args))


def replaceURLs(text):
    return re.sub(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
                  r'<a href="\1">\1</a>', text)


def sha256digest(fname):
    return hashlib.sha256(open(fname, 'rb').read()).hexdigest()
