# -*- coding: utf-8 -*-
import os
import urllib2
import re
import json
import platform
import logging
import logging.handlers
from PyQt4 import QtGui, QtCore
from ggpo.common.settings import Settings


def checkUpdate(self):
    VERSION = 1
    versionurl = ''
    downloadurl = ''
    #noinspection PyBroadException
    try:
        response = urllib2.urlopen(versionurl)
        latestVersion = response.read().strip()
        if latestVersion != VERSION:
            self.sigNewVersionAvailable.emit(latestVersion, downloadurl)
            logger().info("New version " + latestVersion + " available at " + downloadurl)
    except:
        pass


def findURLs(url):
    return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)


def findWine():
    if isWindows():
        return True
    saved = Settings.value(Settings.WINE_LOCATION)
    if saved and os.path.isfile(saved):
        return saved
    w = None
    if isLinux():
        w = '/usr/bin/wine'
    elif isOSX():
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


geoip2Installed = False

try:
    # noinspection PyUnresolvedReferences
    import geoip2.database
    # http://dev.maxmind.com/geoip/geoip2/geolite2/
    # https://github.com/maxmind/GeoIP2-python
    # GeoLite2 databases are updated on the first Tuesday of each month.
    # http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz
    geoip2Installed = True
except ImportError:
    pass


def geolookup(ip):
    db = Settings.value(Settings.GEOIP2DB_LOCATION)
    if not geoip2Installed or not db or not os.path.isfile(db):
        return 'unknown', '', ''
    # noinspection PyBroadException
    try:
        reader = geoip2.database.Reader(db)
        response = reader.city(ip)
        cc = response.country.iso_code.lower()
        return cc, response.country.name, response.city.name
    except:
        return 'unknown', '', ''


def isLinux():
    return platform.system() == 'Linux'


def isOSX():
    return platform.system() == 'Darwin'


def isUnknownCountryCode(cc):
    return not cc or cc == 'unknown'


def isWindows():
    return platform.system() == 'Windows'


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
        'ggpo.log', mode='a', maxBytes=100000, backupCount=4)
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


def replaceURLs(text):
    return re.sub(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
                  r'<a href="\1">\1</a>', text)
