# -*- coding: utf-8 -*-
import pickle
import os.path
from PyQt4.QtCore import QSettings


# noinspection PyClassHasNoInit
class Settings:
    # list of saved setting for autocomplete and avoid typos
    IGNORED = 'ignored'
    SELECTED_CHANNEL = 'channel'
    USERNAME = 'username'
    PASSWORD = 'password'
    SMOOTHING = 'smoothing'
    MUTE_CHALLENGE_SOUND = 'mute'
    NOTIFY_PLAYER_STATE_CHANGE = 'notifyPlayerStateChange'
    WINDOW_GEOMETRY = 'mainWindowGeometry'
    WINDOW_STATE = 'mainWindowState'
    SPLITTER_STATE = 'splitterState'
    TABLE_HEADER_STATE = 'tableHeaderState'
    EMOTICON_DIALOG_GEOMETRY = 'emoticonDialogGeometry'
    COLORTHEME = 'colortheme'
    CUSTOM_THEME_FILENAME = 'customThemeFilename'
    CHAT_HISTORY_FONT = 'chatFont'
    DEBUG_LOG = 'debuglog'
    SAVE_USERNAME_PASSWORD = 'saveUsernameAndPassword'
    GGPOFBA_LOCATION = 'ggpofbaLocation'
    WINE_LOCATION = 'wineLocation'
    GEOIP2DB_LOCATION = 'geoip2dbLocation'
    UNSUPPORTED_GAMESAVES_DIR = 'unsupportedGamesavesDir'

    _settings = QSettings(os.path.join(os.path.expanduser("~"), 'ggpo.ini'), QSettings.IniFormat)

    @staticmethod
    def setBoolean(key, val):
        if val:
            val = '1'
        else:
            val = ''
        Settings._settings.setValue(key, val)

    @staticmethod
    def setPythonValue(key, val):
        try:
            Settings._settings.setValue(key, pickle.dumps(val))
        except pickle.PickleError:
            pass

    @staticmethod
    def pythonValue(key):
        # noinspection PyBroadException
        try:
            return pickle.loads(Settings._settings.value(key))
        except:
            return None

    @staticmethod
    def setValue(key, val):
        Settings._settings.setValue(key, val)

    @staticmethod
    def value(key):
        return Settings._settings.value(key)