# -*- coding: utf-8 -*-
import json
import os
import re
import urllib
import urllib2
import time
from PyQt4 import QtCore
from ggpo.common.util import logger, findUnsupportedGamesavesDir, sha256digest


class SyncWorker(QtCore.QObject):
    sigFinished = QtCore.pyqtSignal()
    sigStatusMessage = QtCore.pyqtSignal(str)
    SAVESTATES_GITHUB_BASE_URL = 'https://raw.github.com/afurlani/ggpostates/master/'
    SAVESTATES_INDEX_URL = SAVESTATES_GITHUB_BASE_URL + 'index.json'

    def download(self):
        d = findUnsupportedGamesavesDir()
        if not d:
            self.sigStatusMessage.emit('Unsupported Savestates Directory is not set')
            self.sigFinished.emit()
            return
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
                localfile = os.path.join(d, filename)
                if os.path.isfile(localfile) and sha256digest(localfile) == shahash:
                    self.sigStatusMessage.emit('{} is update to date'.format(filename))
                    continue
                fileurl = self.SAVESTATES_GITHUB_BASE_URL + urllib.quote(filename)
                time.sleep(0.05)
                urllib.urlretrieve(fileurl, localfile)
                self.sigStatusMessage.emit('Downloaded {}'.format(localfile))
        except Exception, ex:
            logger().error(str(ex))
        self.sigFinished.emit()


# noinspection PyClassHasNoInit
class UnsupportedSavestates:
    _thread = None
    _worker = None

    @classmethod
    def sync(cls, mainWindow):
        if cls._thread:
            logger().error('Already has a download thread running')
        cls._thread = QtCore.QThread()
        cls._worker = SyncWorker()
        cls._worker.moveToThread(cls._thread)
        cls._worker.sigFinished.connect(cls.cleanup)
        cls._worker.sigStatusMessage.connect(mainWindow.onStatusMessage)
        cls._thread.started.connect(cls._worker.download)
        cls._thread.start()

    @classmethod
    def cleanup(cls):
        cls._thread.quit()
        cls._thread.wait()
        cls._thread = None
        cls._worker = None
