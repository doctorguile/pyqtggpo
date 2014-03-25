# -*- coding: utf-8 -*-
from glob import glob
import fnmatch
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import operator
from ggpo.common.allgames import allgames
from ggpo.common.settings import Settings
from ggpo.common.util import findUnsupportedGamesavesDir
from ggpo.gui.ui.savestatesdialog_ui import Ui_SavestatesDialog


class SavestatesModel(QtCore.QAbstractTableModel):
    N_DISPLAY_COLUMNS = 4
    NAME, MANUFACTURER, YEAR, DESCRIPTION, FULLPATH = range(5)

    def __init__(self):
        super(SavestatesModel, self).__init__()
        self.lastSort = self.NAME
        self.lastSortDirection = QtCore.Qt.DescendingOrder
        self.allGames = []
        self.filteredGames = []
        self.scanFsFiles()

    def columnCount(self, parent=None, *args, **kwargs):
        return SavestatesModel.N_DISPLAY_COLUMNS

    def data(self, modelIndex, role=None):
        if not modelIndex.isValid():
            return None
        elif role == Qt.DisplayRole:
            r = modelIndex.row()
            c = modelIndex.column()
            return self.filteredGames[r][c]

    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return super(SavestatesModel, self).flags(index)

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return {0: 'Filename', 1: 'Manufacturer', 2: 'Year', 3: 'Description'}[section]

    def insertFsFile(self, filename):
        name = os.path.splitext(os.path.basename(filename))[0]
        if name in allgames:
            manufacturerYearDesc = allgames[name]
            self.allGames.append([name] + manufacturerYearDesc + [filename])
        else:
            self.allGames.append([name, '', '', '', filename])

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.filteredGames)

    def scanFsFiles(self):
        d = findUnsupportedGamesavesDir()
        if not d:
            return
        for f in glob(os.path.join(d, '*.fs')):
            self.insertFsFile(f)
        self.filteredGames = self.allGames[:]

    def setFilter(self, userFilter):
        if userFilter:
            userFilter = userFilter.strip().lower()
        if not userFilter:
            self.filteredGames = self.allGames[:]
        else:
            if not userFilter.startswith('*'):
                userFilter = '*' + userFilter
            if not userFilter.endswith('*'):
                userFilter += '*'
            self.filteredGames = []
            for d in self.allGames:
                if fnmatch.fnmatch(d[self.NAME].lower(), userFilter) or \
                        fnmatch.fnmatch(d[self.DESCRIPTION].lower(), userFilter):
                    self.filteredGames.append(d)
        self.sort(self.lastSort, self.lastSortDirection)
        rowcount = len(self.filteredGames)
        if rowcount > 0:
            idx1 = self.createIndex(0, 0)
            idx2 = self.createIndex(rowcount - 1, self.N_DISPLAY_COLUMNS - 1)
        else:
            idx1 = idx2 = QtCore.QModelIndex()
        self.dataChanged.emit(idx1, idx2)

    def sort(self, col, order=None):
        reverse = True
        if order == QtCore.Qt.DescendingOrder:
            reverse = False
        self.lastSort = col
        self.lastSortDirection = order
        getter = operator.itemgetter(col)
        keyfunc = lambda x: getter(x).lower()
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.filteredGames.sort(key=keyfunc, reverse=reverse)
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
        self.model.dataChanged.connect(self.onDataChanged)
        self.uiFilterLineEdit.textEdited.connect(self.model.setFilter)
        self.uiSavestatesTblv.setModel(self.model)
        self.uiSavestatesTblv.doubleClicked.connect(self.accept)
        self.uiSavestatesTblv.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.uiSavestatesTblv.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        sm = self.uiSavestatesTblv.selectionModel()
        sm.selectionChanged.connect(self.onSelectionChanged)
        self.uiSavestatesTblv.verticalHeader().setVisible(False)
        hh = self.uiSavestatesTblv.horizontalHeader()
        hh.setStretchLastSection(True)
        hh.setMinimumSectionSize(25)
        hh.setHighlightSections(False)
        hh.resizeSection(SavestatesModel.NAME, 100)
        hh.resizeSection(SavestatesModel.MANUFACTURER, 100)
        hh.resizeSection(SavestatesModel.YEAR, 50)
        self.uiSavestatesTblv.setSortingEnabled(True)
        self.accepted.connect(self.saveGeometrySettings)
        self.finished.connect(self.saveGeometrySettings)
        self.rejected.connect(self.saveGeometrySettings)
        self.restoreStateAndGeometry()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Up, Qt.Key_Down):
            rc = self.model.rowCount()
            if rc:
                idx = None
                sm = self.uiSavestatesTblv.selectionModel()
                if sm.hasSelection():
                    selected = self.uiSavestatesTblv.selectionModel().selectedRows()[0]
                    if e.key() == Qt.Key_Down and selected.row() < rc - 1:
                        idx = self.model.createIndex(selected.row() + 1, 0)
                    elif e.key() == Qt.Key_Up and selected.row() > 0:
                        idx = self.model.createIndex(selected.row() - 1, 0)
                else:
                    row = (e.key() == Qt.Key_Up) and (rc - 1) or 0
                    idx = self.model.createIndex(row, 0)
                if idx:
                    sm.clearSelection()
                    sm.select(idx, QtGui.QItemSelectionModel.Select | QtGui.QItemSelectionModel.Rows)
                    self.uiSavestatesTblv.scrollTo(idx)
                    e.ignore()
                    return
        super(SavestatesDialog, self).keyPressEvent(e)

    def onAccepted(self):
        selected = self.uiSavestatesTblv.selectionModel().selectedRows()[0]
        self.fsfile = self.model.filteredGames[selected.row()][SavestatesModel.FULLPATH]

    def onDataChanged(self, startIdx, endIdx):
        sm = self.uiSavestatesTblv.selectionModel()
        sm.clearSelection()
        if endIdx.isValid() and endIdx.row() == 0:
            sm.select(endIdx, QtGui.QItemSelectionModel.Select | QtGui.QItemSelectionModel.Rows)

    def onSelectionChanged(self):
        self.uiButtonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(
            self.uiSavestatesTblv.selectionModel().hasSelection())

    def restoreStateAndGeometry(self):
        saved = Settings.value(Settings.SAVESTATES_DIALOG_GEOMETRY)
        if saved:
            self.restoreGeometry(saved)
        saved = Settings.value(Settings.SAVESTATES_DIALOG_TABLE_HEADER_STATE)
        if saved:
            self.uiSavestatesTblv.horizontalHeader().restoreState(saved)

    def saveGeometrySettings(self):
        Settings.setValue(Settings.SAVESTATES_DIALOG_GEOMETRY, self.saveGeometry())
        Settings.setValue(Settings.SAVESTATES_DIALOG_TABLE_HEADER_STATE,
                          self.uiSavestatesTblv.horizontalHeader().saveState())
