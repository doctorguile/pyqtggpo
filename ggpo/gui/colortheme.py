# -*- coding: utf-8 -*-
import cgi
from PyQt4 import QtGui
from PyQt4.QtCore import QFile, QIODevice
from ggpo.common.settings import Settings


# noinspection PyClassHasNoInit
class ColorTheme:
    # http://dmcritchie.mvps.org/excel/colors.htm
    LIGHT = {
        'status': 'C0C0C0',
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
        'status': '808080',
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
                   'FFFFFF',
                   '9999FF',
                   'FFFFCC',
                   'CCFFFF',
                   'FF8080',
                   'CCCCFF']
    }

    SELECTED = LIGHT

    @staticmethod
    def getPlayerColor(playerid):
        return '#' + ColorTheme.SELECTED['player'][playerid % ColorTheme.SELECTED['count']]

    @staticmethod
    def setDarkTheme(boolean):
        qss = ''
        if boolean:
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
        else:
            ColorTheme.SELECTED = ColorTheme.LIGHT
            Settings.setValue(Settings.COLORTHEME, '')
        QtGui.QApplication.instance().setStyleSheet(qss)

    @staticmethod
    def statusHtml(txt):
        if txt:
            txt = cgi.escape(txt)
            txt = txt.replace("\n", "<br/>")
            return '<font color="#' + ColorTheme.SELECTED['status'] + '">' + txt + "</font>"


ColorTheme.LIGHT['count'] = len(ColorTheme.LIGHT['player'])
ColorTheme.DARK['count'] = len(ColorTheme.DARK['player'])
