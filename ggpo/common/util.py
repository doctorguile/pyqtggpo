# -*- coding: utf-8 -*-
import hashlib
import logging
import logging.handlers
import os
import re
import sys
import urllib2
from collections import defaultdict
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


def defaultdictinit(startdic):
    if not startdic:
        raise KeyError
    d = None
    for v in startdic.values():
        d = defaultdict(type(v))
        break
    for k, v in startdic.items():
        d[k] = v
    return d


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


def logdebug():
    global _loggerInitialzed
    if not _loggerInitialzed:
        _loggerInitialzed = True
        loggerInit()
    return logging.getLogger('GGPODebug')


def loguser():
    global _loggerInitialzed
    if not _loggerInitialzed:
        _loggerInitialzed = True
        loggerInit()
    return logging.getLogger('GGPOUser')


def loggerInit():
    debuglog = logging.getLogger('GGPODebug')
    debuglog.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler(
        os.path.join(expanduser("~"), 'ggpodebug.log'), mode='a', maxBytes=500000, backupCount=10)
    if Settings.value(Settings.DEBUG_LOG):
        fh.setLevel(logging.INFO)
    else:
        fh.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    debuglog.addHandler(fh)
    debuglog.addHandler(ch)

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        debuglog.error("<Uncaught exception>", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception

    if __name__ == "__main__":
        raise RuntimeError("Test unhandled")

    userlog = logging.getLogger('GGPOUser')
    userlog.setLevel(logging.INFO)
    fh = logging.handlers.RotatingFileHandler(
        os.path.join(expanduser("~"), 'ggpo.log'), mode='a', maxBytes=500000, backupCount=10)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s', "%Y-%m-%d %H:%M")
    fh.setFormatter(formatter)
    userlog.addHandler(fh)


def openURL(url):
    # noinspection PyCallByClass
    QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))


def packagePathJoin(*args):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, *args))


def replaceURLs(text):
    return re.sub(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
                  r'<a href="\1"><font color=green>\1</font></a>', text)


def sha256digest(fname):
    return hashlib.sha256(open(fname, 'rb').read()).hexdigest()
