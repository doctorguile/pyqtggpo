# -*- coding: utf-8 -*-
from glob import glob
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import operator
from ggpo.common.allgames import allgames
from ggpo.common.util import findUnsupportedGamesavesDir
from ggpo.gui.ui.savestatesdialog_ui import Ui_SavestatesDialog


class SavestatesModel(QtCore.QAbstractTableModel):
    N_DISPLAY_COLUMNS = 4
    NAME, MANUFACTURER, YEAR, DESCRIPTION, FULLPATH = range(5)

    def __init__(self):
        super(SavestatesModel, self).__init__()
        self._data = []
        self.scanFs()

    def scanFs(self):
        d = findUnsupportedGamesavesDir()
        if not d:
            return
        for f in glob(os.path.join(d, '*.fs')):
            self.insertFs(f)

    def insertFs(self, f):
        n = os.path.splitext(os.path.basename(f))[0]
        if n in allgames:
            g = allgames[n]
            self._data.append([n] + g + [f])
        else:
            self._data.append([n, '', '', '', f])

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return SavestatesModel.N_DISPLAY_COLUMNS

    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return super(SavestatesModel, self).flags(index)

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return {0: 'Filename', 1: 'Manufacturer', 2: 'Year', 3: 'Description'}[section]

    def data(self, modelIndex, role=None):
        if not modelIndex.isValid():
            return None
        elif role == Qt.DisplayRole:
            r = modelIndex.row()
            c = modelIndex.column()
            return self._data[r][c]

    def sort(self, col, order=None):
        reverse = True
        if order == QtCore.Qt.DescendingOrder:
            reverse = False
        getter = operator.itemgetter(col)
        keyfunc = lambda x: getter(x).lower()
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self._data.sort(key=keyfunc, reverse=reverse)
        self.emit(QtCore.SIGNAL("layoutChanged()"))


class SavestatesDialog(QtGui.QDialog, Ui_SavestatesDialog):
    def __init__(self, *args, **kwargs):
        super(SavestatesDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.fsfile = None
        okbtn = self.uiButtonBox.button(QtGui.QDialogButtonBox.Ok)
        okbtn.setEnabled(False)
        self.accepted.connect(self.onAccepted)
        self.model = SavestatesModel()
        self.uiSavestatesTblv.setModel(self.model)
        self.uiSavestatesTblv.doubleClicked.connect(self.accept)
        self.uiSavestatesTblv.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.uiSavestatesTblv.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        sm = self.uiSavestatesTblv.selectionModel()
        sm.selectionChanged.connect(lambda: okbtn.setEnabled(sm.hasSelection()))
        self.uiSavestatesTblv.verticalHeader().setVisible(False)
        hh = self.uiSavestatesTblv.horizontalHeader()
        hh.setStretchLastSection(True)
        hh.setMinimumSectionSize(25)
        hh.setHighlightSections(False)
        hh.resizeSection(SavestatesModel.NAME, 100)
        hh.resizeSection(SavestatesModel.MANUFACTURER, 100)
        hh.resizeSection(SavestatesModel.YEAR, 50)
        self.uiSavestatesTblv.setSortingEnabled(True)

    def onAccepted(self):
        qModelIndex = self.uiSavestatesTblv.selectionModel().selectedRows()[0]
        self.fsfile = self.model._data[qModelIndex.row()][SavestatesModel.FULLPATH]
