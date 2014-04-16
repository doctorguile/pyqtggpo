# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import base64
import ggpo.gui
from ggpo.common.util import openURL, checkUpdate
from ggpo.common import copyright
from ggpo.common.settings import Settings
from ggpo.gui.ui.logindialog_ui import Ui_DialogLogin


class LoginDialog(QtGui.QDialog, Ui_DialogLogin):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        # ggpo.gui.loadUi(__file__, self)
        self.setupUi(self)
        self.uiNewVersionLink.clicked.connect(
            lambda: openURL('https://github.com/doctorguile/pyqtggpo/releases'))
        self.uiNewVersionLink.setVisible(False)
        versionLabel = 'v' + copyright.versionString()
        self.uiVersionLbl.setText(versionLabel)
        self.controller = None
        if Settings.value(Settings.SAVE_USERNAME_PASSWORD):
            self.uiSavePasswordChk.setChecked(True)
        if Settings.value(Settings.AUTOLOGIN):
            self.uiAutologinChk.setChecked(True)
        username = Settings.value(Settings.USERNAME)
        password = Settings.value(Settings.PASSWORD)
        if username:
            self.uiUsernameLine.setText(username)
        if password:
            self.uiPasswordLine.setText(base64.decodestring(password))
        self.uiSavePasswordChk.toggled.connect(self.savePassword)
        self.uiUsernameLine.returnPressed.connect(self.login)
        self.uiPasswordLine.returnPressed.connect(self.login)
        self.uiLoginBtn.clicked.connect(self.login)
        self.uiRegisterLink.clicked.connect(
            lambda: openURL('http://ggpo.net/forums/ucp.php?mode=register'))

    def displayErrorMessage(self, errmsg):
        self.uiErrorLbl.setText(errmsg)

    def login(self):
        if not self.uiLoginBtn.isEnabled():
            return
        username = self.uiUsernameLine.text().strip()
        password = self.uiPasswordLine.text()
        self.uiErrorLbl.clear()
        errmsg = ''
        if not username:
            errmsg += "Username required\n"
        if not password:
            errmsg += "Password required\n"
        if errmsg:
            self.uiErrorLbl.setText(errmsg)
            return

        if self.uiSavePasswordChk.isChecked():
            Settings.setValue(Settings.USERNAME, username)
            Settings.setValue(Settings.PASSWORD, base64.encodestring(password))
            Settings.setBoolean(Settings.AUTOLOGIN, self.uiAutologinChk.isChecked())
        else:
            Settings.setValue(Settings.USERNAME, '')
            Settings.setValue(Settings.PASSWORD, '')
            Settings.setBoolean(Settings.AUTOLOGIN, False)

        self.uiLoginBtn.setEnabled(False)

        if not self.controller.connectTcp():
            # noinspection PyCallByClass,PyTypeChecker,PyArgumentList
            QtGui.QMessageBox.warning(self, 'Error', "Cannot connect to ggpo.net")
            self.uiLoginBtn.setEnabled(True)
            return -1

        self.controller.sendWelcome()
        self.controller.sendAuth(username, password)

    def onLoginFailed(self):
        self.uiLoginBtn.setEnabled(True)
        self.displayErrorMessage("Invalid username/password")

    def onServerDisconnected(self):
        self.uiLoginBtn.setEnabled(True)
        self.displayErrorMessage("Disconnected from ggpo.net.\nPlease restart application")

    def onStatusMessage(self, msg):
        self.uiLoginBtn.setEnabled(True)
        self.displayErrorMessage(msg)

    # noinspection PyMethodMayBeStatic
    def savePassword(self, value):
        Settings.setBoolean(Settings.SAVE_USERNAME_PASSWORD, value)

    def setController(self, controller):
        self.controller = controller
        controller.sigServerDisconnected.connect(self.onServerDisconnected)
        controller.sigLoginSuccess.connect(self.accept)
        controller.sigLoginFailed.connect(self.onLoginFailed)
        controller.sigStatusMessage.connect(self.onStatusMessage)

    def showEvent(self, QShowEvent):
        QtGui.QDialog.showEvent(self, QShowEvent)
        if checkUpdate():
            self.uiNewVersionLink.setVisible(True)
        if Settings.value(Settings.AUTOLOGIN):
            self.login()