# -*- coding: utf-8 -*-
import cgi
from PyQt4 import QtGui
from PyQt4.QtCore import QFile, QIODevice
from ggpo.common.settings import Settings


# noinspection PyClassHasNoInit
class ColorTheme:
    originalStyle = None
    originalPalette = None

    # http://dmcritchie.mvps.org/excel/colors.htm
    LIGHT = {
        'player': ['993300',
                   '003366',
                   '333399',
                   '800000',
                   'FF6600',
                   '808000',
                   '000080',
                   '008000',
                   '666699',
                   'FF9900',
                   '99CC00',
                   '339966',
                   '33CCCC',
                   '3366FF',
                   '800080',
                   'FF00FF',
                   '00CCFF',
                   '993366',
                   '660066',
                   '0066CC',
                   '008080',
                   '0000FF']
    }

    DARK = {
        'player': ['FF6600',
                   'FF9900',
                   '99CC00',
                   '33CCCC',
                   'FF00FF',
                   'FFCC00',
                   'FFFF00',
                   '00FF00',
                   '00FFFF',
                   '00CCFF',
                   'C0C0C0',
                   'FF99CC',
                   'FFCC99',
                   'FFFF99',
                   'CCFFCC',
                   '99CCFF',
                   'CC99FF',
                   'ECECEC',
                   '9999FF',
                   'FFFFCC',
                   'CCFFFF',
                   'FF8080',
                   'CCCCFF']
    }

    SAFE = {
        'player': ['FF6600', 'CC99FF', '00CCFF', '00FF00',
                    '9999FF', 'FF8080', 'FF00FF', '33CCCC', '99CC00']
    }

    SELECTED = LIGHT

    @staticmethod
    def getPlayerColor(playerid):
        return '#' + ColorTheme.SELECTED['player'][playerid % ColorTheme.SELECTED['count']]

    @classmethod
    def saveDefaultStyle(cls):
        cls.originalStyle = QtGui.QApplication.style().objectName()
        cls.originalPalette = QtGui.QApplication.palette()

    @staticmethod
    def setDarkTheme(boolean):
        if boolean:
            qss = ''
            ColorTheme.SELECTED = ColorTheme.DARK
            Settings.setValue(Settings.COLORTHEME, 'darkorange')
            # noinspection PyBroadException
            try:
                qfile = QFile(':qss/darkorange.qss')
                if qfile.open(QIODevice.ReadOnly | QIODevice.Text):
                    qss = str(qfile.readAll())
                    qfile.close()
            except:
                qss = ''
                pass
            QtGui.QApplication.setStyle(ColorTheme.originalStyle)
            QtGui.QApplication.setPalette(ColorTheme.originalPalette)
            QtGui.QApplication.instance().setStyleSheet(qss)

    @staticmethod
    def setNormalTheme(boolean):
        if boolean:
            ColorTheme.SELECTED = ColorTheme.LIGHT
            QtGui.QApplication.setStyle(ColorTheme.originalStyle)
            QtGui.QApplication.setPalette(ColorTheme.originalPalette)
            Settings.setValue(Settings.COLORTHEME, '')
            QtGui.QApplication.instance().setStyleSheet('')

    @staticmethod
    def statusHtml(txt):
        if txt:
            txt = cgi.escape(txt)
            txt = txt.replace("\n", "<br/>")
            return '<font color="#808080">' + txt + "</font>"


ColorTheme.LIGHT['count'] = len(ColorTheme.LIGHT['player'])
ColorTheme.DARK['count'] = len(ColorTheme.DARK['player'])
ColorTheme.SAFE['count'] = len(ColorTheme.SAFE['player'])
