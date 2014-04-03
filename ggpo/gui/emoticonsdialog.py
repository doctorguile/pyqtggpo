# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ggpo.common.runtime import *
from ggpo.common.settings import Settings

class FlowLayout(QtGui.QLayout):
    def __init__(self, parent=None, margin=10, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setMargin(margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    # noinspection PyMethodMayBeStatic
    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.margin(), 2 * self.margin())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QtGui.QSizePolicy.PushButton,
                                                                QtGui.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QtGui.QSizePolicy.PushButton,
                                                                QtGui.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


_emoticons = r''':-)
:3
:>
=]
8)
=)
;-)
:D
xD
X-D
>:[
:-(
:{
:'(
v.v
:-O
( '}{' )
:P
:-/
o/\o
:-###..
\o/
*\0/*
O.o
ಠ_ಠ
(>_<)
(^_^;)
(-_-;)
(~_~;)
(#^.^#)
(-_-)zzz
(^_-)-☆
((+_+))
(+o+)
<(｀^´)>
^_^
(^O^)
('_')
(ー_ー)!!
(=_=)
(=^・^=)
＼(^o^)／
¯\_(ツ)_/¯
(*_*)
（・∀・）
<`～´>
（*´▽｀*）
(╯°□°）╯︵ ┻━┻ ┬──┬
ありがとう
☼
☽
☂
★
☎
♂
♀
♥
♪
♫
←
↙
↓
↘
→
↗
↑
↖
↺
↓↘→
↓↙←
→↓↘
←↙↓↘→
↙↘↙↗
↙↓↘→↗
↓→↗
←↙↓↘→↗↑↖'''


class EmoticonDialog(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(EmoticonDialog, self).__init__(*args, **kwargs)
        saved = Settings.value(Settings.EMOTICON_DIALOG_GEOMETRY)
        if saved:
            self.restoreGeometry(saved)
        self._value = ''
        flowLayout = FlowLayout(self)
        customEmoticons = Settings.value(Settings.CUSTOM_EMOTICONS)
        if customEmoticons:
            customEmoticons = filter(None, [line.strip()
                                            for line in customEmoticons.split("\n")
                                            if 0 < len(line) < 64])
        else:
            customEmoticons = []
        for emoticon in customEmoticons + _emoticons.split("\n"):
            act = QtGui.QAction(emoticon, self)
            act.triggered.connect(self.onActionTriggered)
            btn = QtGui.QToolButton(self)
            btn.setDefaultAction(act)
            flowLayout.addWidget(btn)
        self.setLayout(flowLayout)
        self.setWindowTitle("Insert emoticon")
        self.accepted.connect(self.saveGeometrySettings)
        self.finished.connect(self.saveGeometrySettings)
        self.rejected.connect(self.saveGeometrySettings)

    def onActionTriggered(self):
        self._value = self.sender().text()
        self.accept()

    def saveGeometrySettings(self):
        Settings.setValue(Settings.EMOTICON_DIALOG_GEOMETRY, self.saveGeometry())

    def value(self):
        return self._value

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = EmoticonDialog()
    mainWin.show()
    sys.exit(app.exec_())
