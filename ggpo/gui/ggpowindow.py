# -*- coding: utf-8 -*-
import cgi
import logging
import logging.handlers
import os
import re
import shutil
from colortheme import ColorTheme
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from ggpo.common.geolookup import geolookupInit
from ggpo.common.runtime import *
from ggpo.common import copyright
from ggpo.common.cliclient import CLI
from ggpo.common.playerstate import PlayerStates
from ggpo.common.settings import Settings
from ggpo.common.util import logger, openURL, findURLs, replaceURLs, findWine, findUnsupportedGamesavesDir, \
    defaultdictinit
from ggpo.common.unsupportedsavestates import UnsupportedSavestates
from ggpo.common.allgames import *
from ggpo.gui.customemoticonsdialog import CustomEmoticonsDialog
from ggpo.gui.emoticonsdialog import EmoticonDialog
from ggpo.gui.playermodel import PlayerModel
from ggpo.gui.savestatesdialog import SavestatesDialog
from ggpo.gui.ui.ggpowindow_ui import Ui_MainWindow


class GGPOWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, QWidget_parent=None):
        super(GGPOWindow, self).__init__(QWidget_parent)
        self.setupUi(self)
        self.controller = None
        self.channels = {}
        self.expectFirstChannelResponse = True
        self.lastSplitterExpandedSizes = []
        self.lastStateChangeMsg = ''
        self.playChallengeSound = lambda: None
        self.uiChatInputEdit.returnPressed.connect(self.returnPressed)
        self.setupMenuAction()
        self.setupMenuSettings()
        self.setupMenuHelp()
        self.uiEmoticonTbtn.setDefaultAction(self.uiEmoticonAct)
        self.uiEmoticonTbtn.setText(':)')
        self.addSplitterHandleToggleButton()
        self.uiChatHistoryTxtB.anchorClicked.connect(self.onAnchorClicked)

    @staticmethod
    def buildInSmoothingToActionName(smooth):
        return 'uiSmoothing{}Act'.format(smooth)

    @staticmethod
    def buildInStyleToActionName(styleName):
        return 'ui{}ThemeAct'.format(re.sub(r'[^a-zA-Z0-9]', '', styleName))

    def onAnchorClicked(self, qurl):
        if qurl.scheme() in ['http', 'https']:
            QtGui.QDesktopServices.openUrl(qurl)
        name = qurl.path()
        if name:
            if qurl.scheme() == 'accept':
                if name in self.controller.challengers:
                    self.controller.sendAcceptChallenge(name)
            elif qurl.scheme() == 'decline':
                if name in self.controller.challengers:
                    self.controller.sendDeclineChallenge(name)
                    self.controller.sigStatusMessage.emit("Declined {}'s challenge".format(name))
                    self.updateStatusBar()

    def onRemoteHasUpdates(self, added, updated, nochange):
        totalchanged = added + updated
        if totalchanged:
            self.uiChatHistoryTxtB.append(ColorTheme.statusHtml(
                "{} savestate(s) added/updated.\nGo to `Action > Sync Unsupported Savestates` for updates".format(
                    totalchanged)))

    def aboutDialog(self):
        QtGui.QMessageBox.information(self, 'About', copyright.about())

    def addSplitterHandleToggleButton(self):
        self.uiSplitter.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        handle = self.uiSplitter.handle(1)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        button = QtGui.QToolButton(handle)
        button.setArrowType(QtCore.Qt.LeftArrow)
        button.clicked.connect(self.onToggleSidebarAction)
        layout.addWidget(button)
        button = QtGui.QToolButton(handle)
        button.setArrowType(QtCore.Qt.RightArrow)
        button.clicked.connect(self.onToggleSidebarAction)
        layout.addWidget(button)
        handle.setLayout(layout)

    def changeFont(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            Settings.setPythonValue(Settings.CHAT_HISTORY_FONT,
                                    [font.family(), font.pointSize(), font.weight(), font.italic()])
            self.uiChatHistoryTxtB.setFont(font)

    def closeEvent(self, evnt):
        Settings.setValue(Settings.WINDOW_GEOMETRY, self.saveGeometry())
        Settings.setValue(Settings.WINDOW_STATE, self.saveState())
        Settings.setValue(Settings.SPLITTER_STATE, self.uiSplitter.saveState())
        Settings.setValue(Settings.TABLE_HEADER_STATE, self.uiPlayersTableV.horizontalHeader().saveState())
        super(GGPOWindow, self).closeEvent(evnt)

    @staticmethod
    def debuglogTriggered(value):
        if value:
            level = logging.INFO
        else:
            level = logging.ERROR
        Settings.setBoolean(Settings.DEBUG_LOG, value)
        for handler in logger().handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.setLevel(level)
                break

    def ignoreAdded(self, name):
        self.uiChatHistoryTxtB.append(ColorTheme.statusHtml("* Adding " + name + " to ignore list."))

    def ignoreRemoved(self, name):
        self.uiChatHistoryTxtB.append(ColorTheme.statusHtml("* Removing " + name + " from ignore list."))

    def insertEmoticon(self):
        dlg = EmoticonDialog(self)
        if dlg.exec_():
            self.uiChatInputEdit.insert(dlg.value())
            self.uiChatInputEdit.setFocus()
            dlg.destroy()

    def joinChannel(self, *args):
        it = self.uiChannelsList.selectedItems()
        if len(it) > 0:
            self.controller.sendJoinChannelRequest(self.channels[it[0].text()])
            self.uiChatInputEdit.setFocus()

    def locateGGPOFBA(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Locate ggpofba.exe', os.path.expanduser("~"),
                                                  "ggpofba.exe (ggpofba.exe)")
        if fname:
            Settings.setValue(Settings.GGPOFBA_LOCATION, fname)
            self.controller.checkInstallation()

    def locateGeoMMDB(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Locate Geo mmdb file', os.path.expanduser("~"),
                                                  "Geo mmdb (*.mmdb)")
        if fname:
            Settings.setValue(Settings.GEOIP2DB_LOCATION, fname)
            geolookupInit()

    def locateUnsupportedSavestatesDirAct(self):
        d = QtGui.QFileDialog.getExistingDirectory(self, "Open Directory",
                                                   os.path.expanduser("~"),
                                                   QtGui.QFileDialog.ShowDirsOnly
                                                   | QtGui.QFileDialog.DontResolveSymlinks)
        if d and os.path.isdir(d):
            Settings.setValue(Settings.UNSUPPORTED_GAMESAVES_DIR, d)

    def locateWine(self):
        if IS_WINDOWS:
            return
        defaultLocation = findWine()
        if not defaultLocation:
            defaultLocation = os.path.expanduser("~")
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Locate wine', defaultLocation, "wine (wine)")
        if fname:
            Settings.setValue(Settings.WINE_LOCATION, fname)

    def notifyStateChange(self, name, msg):
        msg = name + msg
        if self.lastStateChangeMsg != msg:
            self.lastStateChangeMsg = msg
            flag = self.controller.getPlayerFlag(name) or ''
            self.uiChatHistoryTxtB.append(flag + ColorTheme.statusHtml(msg))

    def onActionFailed(self, txt):
        self.uiChatHistoryTxtB.append(ColorTheme.statusHtml(txt))

    def onChallengeCancelled(self, name):
        self.uiChatHistoryTxtB.append(ColorTheme.statusHtml(name + " cancelled challenge"))
        self.updateStatusBar()

    def onChallengeDeclined(self, name):
        self.uiChatHistoryTxtB.append(ColorTheme.statusHtml(name + " declined your challenge"))
        self.updateStatusBar()

    def onChallengeReceived(self, name):
        self.uiChatHistoryTxtB.append(self.controller.getPlayerChallengerText(name))
        self.playChallengeSound()
        self.updateStatusBar()

    def onChatReceived(self, name, txt):
        chat = self.controller.getPlayerPrefix(name, Settings.value(Settings.SHOW_COUNTRY_FLAG_IN_CHAT)) + \
               cgi.escape(txt.strip())
        urls = findURLs(txt)
        if urls:
            for url in urls:
                chat += " <a href='" + url + "'><font color=green>link</font></a>"
        self.uiChatHistoryTxtB.append(chat)

    def onChannelJoined(self):
        self.updateStatusBar()
        if self.controller.channel == 'unsupported':
            UnsupportedSavestates.check(self, self.onStatusMessage, self.onRemoteHasUpdates)

    def onListChannelsReceived(self):
        self.uiChannelsList.clear()
        self.channels = dict((c['title'], c['room']) for c in self.controller.channels.values() if c['room'] != 'lobby')
        sortedRooms = sorted(self.channels.keys())
        if 'lobby' in self.controller.channels:
            title = self.controller.channels['lobby']['title']
            sortedRooms.insert(0, title)
            self.channels[title] = 'lobby'
            self.uiChannelsList.setItemSelected(self.uiChannelsList.item(0), True)
        self.uiChannelsList.addItems(sortedRooms)
        if self.expectFirstChannelResponse:
            self.expectFirstChannelResponse = False
            lastChannel = Settings.value(Settings.SELECTED_CHANNEL)
            if lastChannel in self.controller.channels:
                idx = sortedRooms.index(self.controller.channels[lastChannel]['title'])
                self.uiChannelsList.setItemSelected(self.uiChannelsList.item(0), False)
                self.uiChannelsList.setItemSelected(self.uiChannelsList.item(idx), True)
                self.controller.sendJoinChannelRequest(lastChannel)
        self.uiChannelsList.itemSelectionChanged.connect(self.joinChannel)

    def onMOTDReceived(self, channel, topic, msg):
        self.uiChatHistoryTxtB.setHtml(replaceURLs(msg) + '<br/><br/>Type /help to see a list of commands<br/><br/>')

    def onPlayerStateChange(self, name, state):
        if Settings.value(Settings.NOTIFY_PLAYER_STATE_CHANGE):
            if state == PlayerStates.QUIT:
                self.notifyStateChange(name, " left")
            elif state == PlayerStates.AVAILABLE:
                self.notifyStateChange(name, " becomes available")
            elif state == PlayerStates.PLAYING:
                self.notifyStateChange(name, " is in a game")
        self.updateStatusBar()

    def onStatusMessage(self, msg):
        self.uiChatHistoryTxtB.append(ColorTheme.statusHtml(msg))

    def onToggleSidebarAction(self):
        sizes = self.uiSplitter.sizes()
        if sizes[0]:
            self.lastSplitterExpandedSizes = sizes[:]
            sizes[1] += sizes[0]
            sizes[0] = 0
        else:
            if len(self.lastSplitterExpandedSizes) > 0:
                sizes = self.lastSplitterExpandedSizes
            elif sizes[1]:
                sizes[0] = sizes[1] / 2
                sizes[1] /= 2
        self.uiSplitter.setSizes(sizes)

    def onSplitterHotkeyResizeAction(self, part, growth):
        def resizeCallback():
            increment = 5
            splitterPart, chatHistoryPart, playerViewPart = range(3)
            sizes = self.uiSplitter.sizes()
            if (growth > 0 and sizes[chatHistoryPart] < increment) or \
                    (growth < 0 and sizes[part] == 0):
                return
            total = sizes[part] + sizes[chatHistoryPart]
            if growth < 0:
                increment = min(sizes[part], increment)
                sizes[part] -= increment
                sizes[chatHistoryPart] += increment
            else:
                increment = min(sizes[chatHistoryPart], increment)
                sizes[part] += increment
                sizes[chatHistoryPart] -= increment
            self.uiSplitter.setSizes(sizes)

        return resizeCallback

    def restorePreference(self):
        theme = Settings.value(Settings.COLORTHEME)
        if theme:
            if theme == 'darkorange':
                self.uiDarkThemeAct.setChecked(True)
            elif theme == 'custom':
                fname = Settings.value(Settings.CUSTOM_THEME_FILENAME)
                self.setCustomQssfile(fname)
            else:
                cleanname = self.buildInStyleToActionName(theme)
                if hasattr(self, cleanname):
                    getattr(self, cleanname).setChecked(True)
        smooth = Settings.value(Settings.SMOOTHING)
        if smooth:
            cleanname = self.buildInSmoothingToActionName(smooth)
            if hasattr(self, cleanname):
                getattr(self, cleanname).setChecked(True)
        if Settings.value(Settings.MUTE_CHALLENGE_SOUND):
            self.uiMuteChallengeSoundAct.setChecked(True)
        if Settings.value(Settings.NOTIFY_PLAYER_STATE_CHANGE):
            self.uiNotifyPlayerStateChangeAct.setChecked(True)
        if Settings.value(Settings.SHOW_COUNTRY_FLAG_IN_CHAT):
            self.uiShowCountryFlagInChatAct.setChecked(True)
        fontsetting = Settings.pythonValue(Settings.CHAT_HISTORY_FONT)
        if fontsetting:
            self.uiChatHistoryTxtB.setFont(QtGui.QFont(*fontsetting))
        self.restoreStateAndGeometry()

    def restoreStateAndGeometry(self):
        saved = Settings.value(Settings.WINDOW_GEOMETRY)
        if saved:
            self.restoreGeometry(saved)
        saved = Settings.value(Settings.WINDOW_STATE)
        if saved:
            self.restoreState(saved)
        saved = Settings.value(Settings.SPLITTER_STATE)
        if saved:
            self.uiSplitter.restoreState(saved)
        saved = Settings.value(Settings.TABLE_HEADER_STATE)
        if saved:
            self.uiPlayersTableV.horizontalHeader().restoreState(saved)

    def returnPressed(self):
        line = self.uiChatInputEdit.text().strip()
        if line:
            self.uiChatInputEdit.clear()
            if line[0] == '/':
                if line.startswith('/incoming'):
                    for name in self.controller.challengers:
                        self.uiChatHistoryTxtB.append(self.controller.getPlayerChallengerText(name))
                else:
                    CLI.process(self.controller, self.uiAwayAct.setChecked, line)
            else:
                self.controller.sendChat(line)

    def selectUnsupportedSavestate(self):
        if not self.controller.fba:
            self.onStatusMessage('ggpofba.exe is not set, cannot locate unsupported_ggpo.fs')
            return
        d = findUnsupportedGamesavesDir()
        if not d or not os.path.isdir(d):
            self.onStatusMessage('Unsupported Savestates Directory is not set')
            return
        savestatesDialog = SavestatesDialog()
        if savestatesDialog.exec_():
            fname = savestatesDialog.fsfile
            dst = os.path.join(os.path.dirname(self.controller.fba), 'savestates', 'unsupported_ggpo.fs')
            shutil.copy(fname, dst)
            basefile = os.path.basename(fname)
            basename = os.path.splitext(basefile)[0]
            self.onStatusMessage('Saved {} as unsupported_ggpo.fs'.format(basefile))
            if self.controller.channel == 'unsupported':
                self.controller.setUnsupportedRom('')
                desc = ''
                if basename in allgames:
                    desc = ' {}'.format(allgames[basename][FBA_GAMEDB_DESCRIPTION])
                self.controller.sendChat("* {} switches to [{}]{}".format(self.controller.username, basename, desc))
            self.controller.setUnsupportedRom(basename)

    def setController(self, controller):
        self.controller = controller
        self.setupMediaPlayer()
        self.setupUserTable()
        self.uiChatInputEdit.setController(controller)
        controller.sigChannelJoined.connect(self.onChannelJoined)
        controller.sigPlayersLoaded.connect(self.updateStatusBar)
        controller.sigChannelsLoaded.connect(self.onListChannelsReceived)
        controller.sigMotdReceived.connect(self.onMOTDReceived)
        controller.sigActionFailed.connect(self.onActionFailed)
        controller.sigPlayerStateChange.connect(self.onPlayerStateChange)
        controller.sigChatReceived.connect(self.onChatReceived)
        controller.sigChallengeDeclined.connect(self.onChallengeDeclined)
        controller.sigChallengeReceived.connect(self.onChallengeReceived)
        controller.sigChallengeCancelled.connect(self.onChallengeCancelled)
        controller.sigIgnoreAdded.connect(self.ignoreAdded)
        controller.sigIgnoreRemoved.connect(self.ignoreRemoved)
        controller.sigStatusMessage.connect(self.onStatusMessage)
        controller.sigServerDisconnected.connect(
            lambda: self.onStatusMessage("Disconnected from ggpo.net. Please restart application"))

    def setCustomEmoticons(self):
        dlg = CustomEmoticonsDialog(self)
        if dlg.exec_():
            dlg.destroy()

    def setCustomQss(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Locate Qt Stylesheet qss file', os.path.expanduser("~"),
                                                  "qss file (*.qss)")
        if self.setCustomQssfile(fname):
            for a in self.uiMenuThemeGroup.actions():
                if a.isChecked():
                    a.setChecked(False)

    def setCustomQssfile(self, fname):
        if fname and os.path.isfile(fname):
            # noinspection PyBroadException
            try:
                QtGui.QApplication.instance().setStyleSheet(open(fname).read())
                Settings.setValue(Settings.COLORTHEME, 'custom')
                Settings.setValue(Settings.CUSTOM_THEME_FILENAME, fname)
                ColorTheme.SELECTED = ColorTheme.SAFE
                return True
            except:
                pass

    def setStyleBuiltin(self, styleName):
        if styleName in QtGui.QStyleFactory.keys():
            ColorTheme.SELECTED = ColorTheme.LIGHT
            QtGui.QApplication.instance().setStyleSheet('')
            QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(styleName))
            QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())
            Settings.setValue(Settings.COLORTHEME, styleName)

    def setStyleCallback(self, styleName):
        def setStyle(boolean):
            if boolean:
                self.setStyleBuiltin(styleName)

        return setStyle

    def setupMediaPlayer(self):
        # can't properly install PyQt4.phonon on osx yet
        if IS_OSX:
            self.playChallengeSound = self.controller.playChallengeSound
            return
        try:
            from PyQt4.phonon import Phonon

            audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
            mediaObject = Phonon.MediaObject(self)
            Phonon.createPath(mediaObject, audioOutput)
            mediaObject.setCurrentSource(Phonon.MediaSource(':/assets/challenger-comes.mp3'))

            def play():
                if not Settings.value(Settings.MUTE_CHALLENGE_SOUND):
                    mediaObject.seek(0)
                    mediaObject.play()

            self.playChallengeSound = play
        except ImportError:
            self.playChallengeSound = self.controller.playChallengeSound
            pass

    def setupMenuAction(self):
        self.uiAwayAct.triggered.connect(self.toggleAFK)
        self.uiEmoticonAct.triggered.connect(self.insertEmoticon)
        self.uiToggleSidebarAction.triggered.connect(self.onToggleSidebarAction)
        channelPart, chatHistoryPart, playerViewPart = range(3)
        self.uiContractChannelSidebarAct.triggered.connect(self.onSplitterHotkeyResizeAction(channelPart, -1))
        self.uiExpandChannelSidebarAct.triggered.connect(self.onSplitterHotkeyResizeAction(channelPart, +1))
        self.uiContractPlayerListAct.triggered.connect(self.onSplitterHotkeyResizeAction(playerViewPart, -1))
        self.uiExpandPlayerListAct.triggered.connect(self.onSplitterHotkeyResizeAction(playerViewPart, +1))
        self.uiSelectUnsupportedSavestateAct.triggered.connect(self.selectUnsupportedSavestate)
        self.uiSyncUnsupportedSavestatesAct.triggered.connect(lambda: UnsupportedSavestates.sync(self.onStatusMessage))

    def setupMenuHelp(self):
        self.uiSRKForumAct.triggered.connect(
            lambda: openURL('http://forums.shoryuken.com/categories/super-street-fighter-ii-turbo'))
        self.uiSRKWikiAct.triggered.connect(lambda: openURL('http://wiki.shoryuken.com/Super_Street_Fighter_2_Turbo'))
        self.uiJPWikiAct.triggered.connect(lambda: openURL('http://sf2.gamedb.info/wiki/'))
        self.uiStrevivalAct.triggered.connect(lambda: openURL('http://www.strevival.com/'))
        self.uiHitboxViewerAct.triggered.connect(lambda: openURL('http://www.strevival.com/hitbox/'))
        self.uiSafejumpGuideAct.triggered.connect(lambda: openURL('http://www.strevival.com/hitbox/st-safejump/'))
        self.uiMatchVideosAct.triggered.connect(lambda: openURL('http://www.strevival.com/yt/'))
        self.uiAboutAct.triggered.connect(self.aboutDialog)

    def setupMenuSettings(self):
        self.uiMuteChallengeSoundAct.toggled.connect(self.__class__.toggleSound)
        self.uiFontAct.triggered.connect(self.changeFont)
        self.setupMenuTheme()
        self.setupMenuSmoothing()
        self.uiCustomEmoticonsAct.triggered.connect(self.setCustomEmoticons)

        self.uiLocateGgpofbaAct.triggered.connect(self.locateGGPOFBA)
        if IS_WINDOWS:
            self.uiLocateWineAct.setVisible(False)
        else:
            self.uiLocateWineAct.triggered.connect(self.locateWine)
        self.uiLocateUnsupportedSavestatesDirAct.triggered.connect(self.locateUnsupportedSavestatesDirAct)
        if GeoIP2Reader:
            self.uiLocateGeommdbAct.triggered.connect(self.locateGeoMMDB)
        else:
            self.uiLocateGeommdbAct.setVisible(False)
        self.uiNotifyPlayerStateChangeAct.toggled.connect(self.__class__.toggleNotifyPlayerStateChange)
        self.uiShowCountryFlagInChatAct.toggled.connect(self.__class__.toggleShowCountryFlagInChat)
        if Settings.value(Settings.DEBUG_LOG):
            self.uiDebugLogAct.setChecked(True)
        self.uiDebugLogAct.triggered.connect(self.__class__.debuglogTriggered)

    def setupMenuSmoothing(self):
        # unfortunately Qt Designer doesn't support QActionGroup, we have to code it up
        self.uiMenuSmoothingGroup = QtGui.QActionGroup(self.uiSmoothingMenu, exclusive=True)
        def onSmoothingToggled(boolean):
            if boolean:
                result = re.search(r'[0-9]+', self.sender().text())
                if result:
                    Settings.setValue(Settings.SMOOTHING, result.group(0))
        desc = defaultdictinit({0: ' More jerky', 1: ' Default', 10: ' Laggy'})
        for smooth in range(11):
            act = QtGui.QAction('&' + str(smooth) + desc[smooth], self)
            act.setCheckable(True)
            act.toggled.connect(onSmoothingToggled)
            self.uiSmoothingMenu.addAction(self.uiMenuSmoothingGroup.addAction(act))
            cleanname = self.buildInSmoothingToActionName(smooth)
            setattr(self, cleanname, act)

    def setupMenuTheme(self):
        # unfortunately Qt Designer doesn't support QActionGroup, we have to code it up
        actionTitleShortcuts = set()

        def actionTitle(title):
            shortcutFound = False
            ret = ''
            for c in title:
                l = c.lower()
                if not shortcutFound and l in 'abcdefghijklmnopqrstuvwxy' and l not in actionTitleShortcuts:
                    ret += '&'
                    actionTitleShortcuts.add(l)
                    shortcutFound = True
                ret += c
            return ret

        self.uiMenuThemeGroup = QtGui.QActionGroup(self.uiThemeMenu, exclusive=True)
        self.uiDarkThemeAct = QtGui.QAction(actionTitle("Dark Orange"), self)
        self.uiDarkThemeAct.setCheckable(True)
        self.uiDarkThemeAct.toggled.connect(ColorTheme.setDarkTheme)
        self.uiThemeMenu.addAction(self.uiMenuThemeGroup.addAction(self.uiDarkThemeAct))
        for k in QtGui.QStyleFactory.keys():
            act = QtGui.QAction(actionTitle(k), self)
            act.setCheckable(True)
            act.toggled.connect(self.setStyleCallback(k))
            self.uiThemeMenu.addAction(self.uiMenuThemeGroup.addAction(act))
            cleanname = self.buildInStyleToActionName(k)
            setattr(self, cleanname, act)
        self.uiCustomQssFileAct = QtGui.QAction(actionTitle("Custom Qss stylesheet"), self)
        self.uiCustomQssFileAct.triggered.connect(self.setCustomQss)
        self.uiThemeMenu.addAction(self.uiCustomQssFileAct)

    def setupUserTable(self):
        model = PlayerModel(self.controller)
        self.uiPlayersTableV.setModel(model)
        self.uiPlayersTableV.clicked.connect(model.onCellClicked)
        self.uiPlayersTableV.doubleClicked.connect(model.onCellDoubleClicked)
        self.uiPlayersTableV.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.uiPlayersTableV.verticalHeader().setVisible(False)
        hh = self.uiPlayersTableV.horizontalHeader()
        hh.setMinimumSectionSize(25)
        hh.setHighlightSections(False)
        hh.resizeSection(PlayerModel.STATE, 25)
        width = hh.fontMetrics().boundingRect('Ping').width() + 18
        # windows's sort indicator is displayed at the top so no extra space needed
        if not IS_WINDOWS:
            width += 10
        hh.resizeSection(PlayerModel.PING, width)
        hh.resizeSection(PlayerModel.IGNORE, 25)
        hh.resizeSection(PlayerModel.PLAYER, 165)
        hh.resizeSection(PlayerModel.OPPONENT, 165)
        hh.setResizeMode(PlayerModel.STATE, QtGui.QHeaderView.Fixed)
        hh.setResizeMode(PlayerModel.PING, QtGui.QHeaderView.Fixed)
        hh.setResizeMode(PlayerModel.IGNORE, QtGui.QHeaderView.Fixed)
        self.uiPlayersTableV.setSortingEnabled(True)
        self.uiPlayersTableV.sortByColumn(PlayerModel.DEFAULT_SORT, Qt.AscendingOrder)
        hh.sortIndicatorChanged.connect(self.sortIndicatorChanged)

    def sortIndicatorChanged(self, index, order):
        if index not in self.uiPlayersTableV.model().sortableColumns:
            self.uiPlayersTableV.horizontalHeader().setSortIndicator(
                self.uiPlayersTableV.model().lastSort, self.uiPlayersTableV.model().lastSortOrder)

    def toggleAFK(self, state):
        self.controller.sendToggleAFK(state)

    @staticmethod
    def toggleNotifyPlayerStateChange(state):
        Settings.setBoolean(Settings.NOTIFY_PLAYER_STATE_CHANGE, state)

    @staticmethod
    def toggleShowCountryFlagInChat(state):
        Settings.setBoolean(Settings.SHOW_COUNTRY_FLAG_IN_CHAT, state)

    @staticmethod
    def toggleSound(state):
        Settings.setBoolean(Settings.MUTE_CHALLENGE_SOUND, state)

    def updateStatusBar(self):
        self.uiStatusbar.showMessage(self.controller.statusBarMessage())