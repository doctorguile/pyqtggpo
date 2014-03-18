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
