# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ggpo/gui/ui/customemoticondialog.ui'
#
# Created: Sat Mar 22 15:37:32 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EmoticonDialog(object):
    def setupUi(self, EmoticonDialog):
        EmoticonDialog.setObjectName(_fromUtf8("EmoticonDialog"))
        EmoticonDialog.resize(300, 500)
        self.verticalLayout = QtGui.QVBoxLayout(EmoticonDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(EmoticonDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.uiEmoticonTextEdit = QtGui.QTextEdit(EmoticonDialog)
        self.uiEmoticonTextEdit.setObjectName(_fromUtf8("uiEmoticonTextEdit"))
        self.verticalLayout.addWidget(self.uiEmoticonTextEdit)
        self.buttonBox = QtGui.QDialogButtonBox(EmoticonDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EmoticonDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EmoticonDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EmoticonDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EmoticonDialog)

    def retranslateUi(self, EmoticonDialog):
        EmoticonDialog.setWindowTitle(QtGui.QApplication.translate("EmoticonDialog", "Custom Emoticons", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("EmoticonDialog", "One emoticon per line", None, QtGui.QApplication.UnicodeUTF8))

