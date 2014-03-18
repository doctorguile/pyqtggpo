# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt, QAbstractItemModel, QModelIndex, QEvent
from PyQt4.QtGui import QLineEdit, QCompleter
from ggpo.common.cliclient import CLI
from ggpo.common.playerstate import PlayerStates


class PlayerNameCompletionModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(PlayerNameCompletionModel, self).__init__(parent)
        self.controller = None
        self._prefix = ''
        self._data = CLI.commands.keys()
        self._filtered = self._data
        self._rowcount = len(self._data)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        if index.isValid() and role in [Qt.DisplayRole, Qt.EditRole]:
            row = index.row()
            col = index.column()
            if col == 0 and 0 <= row < self.rowCount():
                return self._filtered[row]

    def index(self, row, column, parent=None, *args, **kwargs):
        if column == 0:
            if 0 <= row < self.rowCount():
                return self.createIndex(row, column)
        return QModelIndex()

    def parent(self, childIndex=None):
        return QModelIndex()

    def playerStateChange(self, name, state):
        if state == PlayerStates.AVAILABLE and name not in self._data:
            self._data.append(name)
            self._filtered = self._data
            self._rowcount = len(self._data)
            # noinspection PyUnresolvedReferences
            self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self._rowcount - 1, 0))

    def playersLoaded(self):
        self._data = CLI.commands.keys() + \
                     [p for p in self.controller.available.keys()] + \
                     [p for p, p2 in self.controller.playing.items()] + \
                     [p for p in self.controller.awayfromkb.keys()]
        self._filtered = self._data
        self._rowcount = len(self._data)

    def rowCount(self, parent=None, *args, **kwargs):
        return self._rowcount

    def setController(self, controller):
        self.controller = controller
        controller.sigPlayersLoaded.connect(self.playersLoaded)
        controller.sigPlayerStateChange.connect(self.playerStateChange)

    def setFilter(self, prefix):
        self._prefix = prefix.lower()
        self._filtered = [x for x in self._data if x.lower().find(self._prefix) != -1]
        self._rowcount = len(self._filtered)
        # noinspection PyUnresolvedReferences
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self._rowcount - 1, 0))


class PlayerNameCompleter(QCompleter):
    def __init__(self, parent=None):
        super(PlayerNameCompleter, self).__init__(parent)
        self.setModel(PlayerNameCompletionModel())
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)

    def update(self, completionText):
        self.model().setFilter(completionText)
        return self.model().rowCount()


class CompletionLineEdit(QLineEdit):
    NON_ALPHA = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="

    def __init__(self, parent=None):
        super(CompletionLineEdit, self).__init__(parent)
        self._completer = PlayerNameCompleter()
        self._completer.setWidget(self)
        # noinspection PyUnresolvedReferences
        self._completer.activated.connect(self.insertCompletion)

    def completer(self):
        return self._completer

    def event(self, evt):
        if (evt.type() == QEvent.KeyPress) and (evt.key() == Qt.Key_Tab):
            if self._completer.popup().isVisible():
                completion = None
                model = self._completer.model()
                selmodel = self._completer.popup().selectionModel()
                selectedIndexes = selmodel.selectedIndexes()
                if selectedIndexes:
                    # user highlighted one of the completion
                    completion = model.data(selectedIndexes[0], Qt.EditRole)
                else:
                    # non empty list of completions to choose from and user hit Tab
                    # we pick the first one for them
                    if model.rowCount() > 0:
                        completion = model.data(model.index(0, 0), Qt.EditRole)
                if completion:
                    self._completer.popup().close()
                    self.insertCompletion(completion)
                    return True
        return QLineEdit.event(self, evt)

    def insertCompletion(self, string):
        if string:
            self.cursorWordBackward(False)
            self.cursorWordForward(True)
            self.del_()
            if string[0] in self.NON_ALPHA:
                string = string[1:]
            self.insert(string + ' ')

    def keyPressEvent(self, e):
        if self._completer and self._completer.popup().isVisible():
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                return

        super(CompletionLineEdit, self).keyPressEvent(e)

        if e.modifiers() & (Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier):
            return

        textUnderCursor = self.textUnderCursor()
        if not e.text() or len(textUnderCursor) < 2 or e.text()[-1] in self.NON_ALPHA:
            self._completer.popup().hide()
            return
        if self._completer.update(textUnderCursor):
            cr = self.cursorRect()
            cr.setWidth(self._completer.popup().sizeHintForColumn(0) +
                        self._completer.popup().verticalScrollBar().sizeHint().width())
            self._completer.complete(cr)
        else:
            self._completer.popup().hide()

    def setController(self, controller):
        self._completer.model().setController(controller)

    def textUnderCursor(self):
        c = self.cursorPosition()
        self.cursorWordBackward(False)
        self.cursorWordForward(True)
        t = self.selectedText()
        self.setCursorPosition(c)
        return t

