# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ggpo/gui/ui/savestatesdialog.ui'
#
# Created: Tue Mar 25 13:27:03 2014
#      by: PyQt4 UI code generator 4.8.5
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
        SavestatesDialog.setWindowTitle(QtGui.QApplication.translate("SavestatesDialog", "Unsupported game savestates", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(SavestatesDialog)
        self.verticalLayout.setContentsMargins(2, 0, 2, 6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(SavestatesDialog)
        self.label.setText(QtGui.QApplication.translate("SavestatesDialog", "Filter:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.uiFilterLineEdit = QtGui.QLineEdit(SavestatesDialog)
        self.uiFilterLineEdit.setText(_fromUtf8(""))
        self.uiFilterLineEdit.setObjectName(_fromUtf8("uiFilterLineEdit"))
        self.horizontalLayout.addWidget(self.uiFilterLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        SavestatesDialog.setTabOrder(self.uiFilterLineEdit, self.uiSavestatesTblv)
        SavestatesDialog.setTabOrder(self.uiSavestatesTblv, self.uiButtonBox)

    def retranslateUi(self, SavestatesDialog):
        pass

