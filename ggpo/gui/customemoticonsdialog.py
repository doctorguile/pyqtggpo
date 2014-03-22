# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ggpo.common.settings import Settings
from ggpo.gui.ui.customemoticonsdialog_ui import Ui_EmoticonDialog


class CustomEmoticonsDialog(QtGui.QDialog, Ui_EmoticonDialog):
    def __init__(self, *args, **kwargs):
        super(CustomEmoticonsDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        customEmoticons = Settings.value(Settings.CUSTOM_EMOTICONS)
        if customEmoticons:
            self.uiEmoticonTextEdit.setPlainText(customEmoticons)
        self.accepted.connect(self.onAccepted)

    def onAccepted(self):
        customEmoticons = self.uiEmoticonTextEdit.toPlainText()
        if customEmoticons:
            saved = "\n".join(filter(None, [line.strip()
                                            for line in customEmoticons.split("\n")
                                            if 0 < len(line) < 64]))
            Settings.setValue(Settings.CUSTOM_EMOTICONS, saved)