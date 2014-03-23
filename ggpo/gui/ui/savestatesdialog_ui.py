# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ggpo/gui/ui/savestatesdialog.ui'
#
# Created: Sun Mar 23 16:16:20 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SavestatesDialog(object):
    def setupUi(self, SavestatesDialog):
        SavestatesDialog.setObjectName(_fromUtf8("SavestatesDialog"))
        SavestatesDialog.resize(630, 600)
        self.verticalLayout = QtGui.QVBoxLayout(SavestatesDialog)
        self.verticalLayout.setContentsMargins(2, 0, 2, 6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.uiSavestatesTblv = QtGui.QTableView(SavestatesDialog)
        self.uiSavestatesTblv.setObjectName(_fromUtf8("uiSavestatesTblv"))
        self.verticalLayout.addWidget(self.uiSavestatesTblv)
        self.uiButtonBox = QtGui.QDialogButtonBox(SavestatesDialog)
        self.uiButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.uiButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.uiButtonBox.setObjectName(_fromUtf8("uiButtonBox"))
        self.verticalLayout.addWidget(self.uiButtonBox)

        self.retranslateUi(SavestatesDialog)
        QtCore.QObject.connect(self.uiButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SavestatesDialog.accept)
        QtCore.QObject.connect(self.uiButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SavestatesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SavestatesDialog)

    def retranslateUi(self, SavestatesDialog):
        SavestatesDialog.setWindowTitle(QtGui.QApplication.translate("SavestatesDialog", "Unsupported game savestates", None, QtGui.QApplication.UnicodeUTF8))

