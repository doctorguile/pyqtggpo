# -*- coding: utf-8 -*-
import operator

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt


#noinspection PyClassHasNoInit
class PlayerModelState:
    AVAILABLE = 0
    PLAYING = 1
    AFK = 2
    NSTATES = 3


class PlayerModel(QtCore.QAbstractTableModel):
    STATE = 0
    PLAYER = 1
    PING = 2
    OPPONENT = 3
    IGNORE = 4
    COUNTRY = 5
    OPPONENT_COUNTRY = 6
    N_COLS = 7

    DEFAULT_SORT = PLAYER

    # state, player, ping, opponent, ignore, accept challenge, decline challenge
    displayColumns = ["", "Player", "Ping", "Opponent", "", "", ""]
    ACCEPT_CHALLENGE = 5
    DECLINE_CHALLENGE = 6
    N_DISPLAY_COLS = len(displayColumns)

    sortableColumns = [PLAYER, PING, OPPONENT]

    def __init__(self, controller):
        super(PlayerModel, self).__init__()
        self.controller = controller
        # [state, player, ping, opponent, ignored, country, opponent_country]
        self.players = []
        self.lastSort = PlayerModel.DEFAULT_SORT
        self.lastSortOrder = QtCore.Qt.AscendingOrder
        controller.sigPlayerStateChange.connect(self.reloadPlayers)
        controller.sigPlayersLoaded.connect(self.reloadPlayers)
        # TODO: optimize to only update challenge column?
        controller.sigChallengeDeclined.connect(self.reloadPlayers)
        controller.sigChallengeReceived.connect(self.reloadPlayers)
        controller.sigChallengeCancelled.connect(self.reloadPlayers)

    # noinspection PyMethodMayBeStatic
    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return PlayerModel.N_DISPLAY_COLS

    def data(self, modelIndex, role=None):
        if not modelIndex.isValid():
            return None

        row = modelIndex.row()
        col = modelIndex.column()

        if role == Qt.DisplayRole:
            if col in [PlayerModel.PLAYER, PlayerModel.PING, PlayerModel.OPPONENT]:
                return self.players[row][col]
        elif role == Qt.ToolTipRole and col in [PlayerModel.PLAYER, PlayerModel.OPPONENT]:
            name = self.players[row][col]
            if name in self.controller.players:
                if self.controller.players[name].city:
                    return self.controller.players[name].country + ', ' + self.controller.players[name].city
                else:
                    return self.controller.players[name].country

        elif role == Qt.CheckStateRole and col == PlayerModel.IGNORE:
            return self.players[row][col]
        elif role == Qt.DecorationRole:
            return self.dataIcon(row, col)
        elif role == Qt.TextAlignmentRole:
            if col == PlayerModel.PING:
                return Qt.AlignRight | Qt.AlignVCenter
        elif role == Qt.TextColorRole:
            if col in [PlayerModel.PLAYER, PlayerModel.OPPONENT]:
                name = self.players[row][col]
                if name == 'ponder':
                    return QtGui.QBrush(QtGui.QColor(Qt.red))

    def dataIcon(self, row, col):
        icon_path = None
        if col == PlayerModel.PLAYER:
            icon_path = ':/flags/' + self.players[row][PlayerModel.COUNTRY] + '.png'
        elif col == PlayerModel.OPPONENT:
            icon_path = ':/flags/' + self.players[row][PlayerModel.OPPONENT_COUNTRY] + '.png'
        elif col == PlayerModel.ACCEPT_CHALLENGE:
            if self.players[row][PlayerModel.PLAYER] in self.controller.challengers:
                icon_path = ':/images/sword-yes.png'
        elif col == PlayerModel.DECLINE_CHALLENGE:
            if self.players[row][PlayerModel.PLAYER] in self.controller.challengers:
                icon_path = ':/images/sword-no.png'
        elif col == PlayerModel.STATE:
            val = self.players[row][col]
            if self.controller.challenged:
                if self.players[row][PlayerModel.PLAYER] == self.controller.challenged:
                    icon_path = ':/images/sword-no.png'
                elif val == PlayerModelState.PLAYING:
                    icon_path = ':/images/eye.png'
                elif val == PlayerModelState.AFK:
                    icon_path = ':/assets/face-sleeping.png'
            else:
                if val == PlayerModelState.AVAILABLE:
                    icon_path = ':/images/sword.png'
                elif val == PlayerModelState.PLAYING:
                    icon_path = ':/images/eye.png'
                elif val == PlayerModelState.AFK:
                    icon_path = ':/assets/face-sleeping.png'
        if icon_path:
            return QtGui.QIcon(icon_path)

    def flags(self, index):
        if index.isValid():
            if index.column() == PlayerModel.IGNORE:
                return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable
            else:
                return Qt.ItemIsEnabled
        return super(PlayerModel, self).flags(index)

    def getPlayerStat(self, player, stat):
        if player in self.controller.players:
            if hasattr(self.controller.players[player], stat):
                return getattr(self.controller.players[player], stat)
        return ''

    # noinspection PyMethodMayBeStatic
    def headerData(self, section, Qt_Orientation, role=None):
        if role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal and 0 <= section < PlayerModel.N_DISPLAY_COLS:
            return PlayerModel.displayColumns[section]
        if role == Qt.DecorationRole and Qt_Orientation == Qt.Horizontal:
            if section == PlayerModel.IGNORE:
                return QtGui.QIcon(':/assets/face-ignore.png')

    def onCellClicked(self, index):
        col = index.column()
        row = index.row()
        if col == PlayerModel.STATE:
            modified = False
            if self.controller.challenged == self.players[row][PlayerModel.PLAYER]:
                self.controller.sendCancelChallenge()
                modified = True
            elif self.players[row][PlayerModel.STATE] == PlayerModelState.AVAILABLE:
                self.controller.sendChallenge(self.players[row][PlayerModel.PLAYER])
                modified = True
            elif self.players[row][PlayerModel.STATE] == PlayerModelState.PLAYING:
                self.controller.sendSpectateRequest(self.players[row][PlayerModel.PLAYER])
                modified = True
            if modified:
                idx1 = self.createIndex(0, PlayerModel.STATE)
                idx2 = self.createIndex(len(self.players) - 1, PlayerModel.STATE)
                # noinspection PyUnresolvedReferences
                self.dataChanged.emit(idx1, idx2)
        if col in [PlayerModel.ACCEPT_CHALLENGE, PlayerModel.DECLINE_CHALLENGE]:
            if col == PlayerModel.ACCEPT_CHALLENGE:
                self.controller.sendAcceptChallenge(self.players[row][PlayerModel.PLAYER])
            elif col == PlayerModel.DECLINE_CHALLENGE:
                self.controller.sendDeclineChallenge(self.players[row][PlayerModel.PLAYER])
            idx1 = self.createIndex(0, PlayerModel.ACCEPT_CHALLENGE)
            idx2 = self.createIndex(len(self.players) - 1, PlayerModel.DECLINE_CHALLENGE)
            # noinspection PyUnresolvedReferences
            self.dataChanged.emit(idx1, idx2)

    # noinspection PyUnusedLocal
    def reloadPlayers(self, *args):
        self.players = []
        for p in self.controller.available.keys():
            ignored = (p in self.controller.ignored) and Qt.Checked or Qt.Unchecked
            self.players.append([PlayerModelState.AVAILABLE,
                                 p, self.getPlayerStat(p, 'ping'),
                                 '', ignored,
                                 self.getPlayerStat(p, 'cc'), ''])
        for p, p2 in self.controller.playing.items():
            ignored = (p in self.controller.ignored) and Qt.Checked or Qt.Unchecked
            self.players.append([PlayerModelState.PLAYING,
                                 p, self.getPlayerStat(p, 'ping'),
                                 p2, ignored,
                                 self.getPlayerStat(p, 'cc'),
                                 self.getPlayerStat(p2, 'cc')])
        for p in self.controller.awayfromkb.keys():
            ignored = (p in self.controller.ignored) and Qt.Checked or Qt.Unchecked
            self.players.append([PlayerModelState.AFK,
                                 p, self.getPlayerStat(p, 'ping'),
                                 '', ignored,
                                 self.getPlayerStat(p, 'cc'), ''])
        self.sort(self.lastSort, self.lastSortOrder)
        # idx1 = self.createIndex(0, 0)
        # idx2 = self.createIndex(len(self.players) - 1, PlayerModel.N_DISPLAY_COLS-1)
        # self.dataChanged.emit(idx1, idx2)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.players)

    def setData(self, modelIndex, value, role=None):
        row = modelIndex.row()
        col = modelIndex.column()
        if role == Qt.CheckStateRole and col == PlayerModel.IGNORE:
            self.players[row][col] = value
            # noinspection PyUnresolvedReferences
            self.dataChanged.emit(modelIndex, modelIndex)
            player = self.players[row][PlayerModel.PLAYER]
            if player != self.controller.username:
                if value == Qt.Checked:
                    self.controller.addIgnore(player)
                else:
                    self.controller.removeIgnore(player)
        return True

    def sort(self, col, order=None):
        if col in PlayerModel.sortableColumns:
            reverse = False
            if order == QtCore.Qt.DescendingOrder:
                reverse = True
            self.lastSort = col
            self.lastSortOrder = order
            getter = operator.itemgetter(col)
            if col in [PlayerModel.PLAYER, PlayerModel.OPPONENT]:
                keyfunc = lambda x: getter(x).lower()
            else:
                keyfunc = getter
            self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
            self.players = sorted(self.players, key=keyfunc, reverse=reverse)
            self.players = sorted(self.players, key=operator.itemgetter(PlayerModel.STATE))
            self.emit(QtCore.SIGNAL("layoutChanged()"))