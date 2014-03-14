#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sip,sys
# Tell qt to return python string instead of QString
# These are only needed for Python v2 but are harmless for Python v3.
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui, QtCore
# noinspection PyUnresolvedReferences
import ggpo.resources.ggpo_rc

app = QtGui.QApplication(sys.argv)
app.setOrganizationName("GGPO")
QtCore.QCoreApplication.setApplicationName("GGPO")

from PyQt4.phonon import Phonon
audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
mediaObject = Phonon.MediaObject()
Phonon.createPath(mediaObject, audioOutput)
mediaObject.setCurrentSource(Phonon.MediaSource(':/assets/challenger-comes.mp3'))

mediaObject.seek(0)
mediaObject.play()

app.exec_()

