# -*- coding: utf-8 -*-
import glob
import hashlib
import json
import os
import re
import urllib
import urllib2
import time
from PyQt4 import QtCore
from ggpo.common.util import logger, findUnsupportedGamesavesDir, sha256digest


class SyncWorker(QtCore.QObject):
    sigFinished = QtCore.pyqtSignal(int, int, int)
    sigStatusMessage = QtCore.pyqtSignal(str)
    SAVESTATES_GITHUB_BASE_URL = 'https://raw.github.com/afurlani/ggpostates/master/'
    JSON_INDEX_FILENAME = 'index.json'
    SAVESTATES_INDEX_URL = SAVESTATES_GITHUB_BASE_URL + JSON_INDEX_FILENAME

    def __init__(self, checkonly=False):
        QtCore.QObject.__init__(self)
        self.checkonly = checkonly
        self.added = 0
        self.updated = 0
        self.nochange = 0
        self.localJsonDigest = {}

    def download(self):
        d = findUnsupportedGamesavesDir()
        if not d:
            self.sigStatusMessage.emit('Unsupported Savestates Directory is not set')
            self.sigFinished.emit(self.added, self.updated, self.nochange)
            return
        self.readLocalJsonDigest()
        # noinspection PyBroadException
        try:
            # gotta love CPython's GIL, yield thread
            time.sleep(0.05)
            response = urllib2.urlopen(self.SAVESTATES_INDEX_URL, timeout=3)
            games = json.load(response)

            for filename, shahash in games.items():
                if re.search(r'[^ .a-zA-Z0-9_-]', filename):
                    logger().error("Filename {} looks suspicious, ignoring".format(filename))
                    continue
                if filename in self.localJsonDigest:
                    if self.localJsonDigest[filename] == shahash:
                        self.nochange += 1
                        continue
                    else:
                        self.updated += 1
                else:
                    self.added += 1
                if not self.checkonly:
                    time.sleep(0.05)
                    localfile = os.path.join(d, filename)
                    fileurl = self.SAVESTATES_GITHUB_BASE_URL + urllib.quote(filename)
                    urllib.urlretrieve(fileurl, localfile)
                    self.sigStatusMessage.emit('Downloaded {}'.format(localfile))
            if not self.checkonly:
                if not self.added and not self.updated:
                    self.sigStatusMessage.emit('All files are up to date')
                else:
                    self.writeLocalJsonDigest()
                    self.sigStatusMessage.emit(
                        '{} files are current, added {}, updated {}'.format(
                            self.nochange, self.added, self.updated))
        except Exception, ex:
            logger().error(str(ex))
        self.sigFinished.emit(self.added, self.updated, self.nochange)

    def readLocalJsonDigest(self):
        d = findUnsupportedGamesavesDir()
        if d:
            localjson = os.path.join(d, self.JSON_INDEX_FILENAME)
            if os.path.isfile(localjson):
                # noinspection PyBroadException
                try:
                    self.localJsonDigest = json.load(file(localjson).read())
                except:
                    pass
            if not self.localJsonDigest:
                self.writeLocalJsonDigest()

    def writeLocalJsonDigest(self):
        d = findUnsupportedGamesavesDir()
        if d:
            localjson = os.path.join(d, self.JSON_INDEX_FILENAME)
            self.localJsonDigest = {}
            for filename in glob.glob(os.path.join(d, '*.fs')):
                self.localJsonDigest[os.path.basename(filename)] = sha256digest(filename)
            # noinspection PyBroadException
            try:
                f = open(localjson, 'w')
                f.write(json.dumps(self.localJsonDigest, sort_keys=True, indent=2))
            except:
                pass


# noinspection PyClassHasNoInit
class UnsupportedSavestates(QtCore.QObject):
    sigRemoteHasUpdates = QtCore.pyqtSignal(int, int, int)

    _thread = None
    _worker = None

    @classmethod
    def check(cls, mainWindow, statusMsgCallback=None, finishedCallback=None):
        cls.run(True, statusMsgCallback, finishedCallback)

    @classmethod
    def cleanup(cls, x, y, z):
        cls._thread.quit()
        cls._thread.wait()
        cls._thread = None
        cls._worker = None

    @classmethod
    def run(cls, checkonly, statusMsgCallback=None, finishedCallback=None):
        if cls._thread:
            logger().error('Already has a download thread running')
        cls._thread = QtCore.QThread()
        cls._worker = SyncWorker(checkonly)
        cls._worker.moveToThread(cls._thread)
        if finishedCallback:
            cls._worker.sigFinished.connect(finishedCallback)
        cls._worker.sigFinished.connect(cls.cleanup)
        if statusMsgCallback:
            cls._worker.sigStatusMessage.connect(statusMsgCallback)
        cls._thread.started.connect(cls._worker.download)
        cls._thread.start()

    @classmethod
    def sync(cls, statusMsgCallback=None, finishedCallback=None):
        cls.run(False, statusMsgCallback, finishedCallback)

