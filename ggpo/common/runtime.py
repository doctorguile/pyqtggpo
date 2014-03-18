# -*- coding: utf-8 -*-
import platform

__all__ = ['IS_WINDOWS', 'IS_OSX', 'IS_LINUX', 'Phonon', 'GeoIP2Reader', 'winsound']

IS_WINDOWS = False
IS_OSX = False
IS_LINUX = False

_platform = platform.system()
if _platform == 'Windows':
    IS_WINDOWS = True
elif _platform == 'Darwin':
    IS_OSX = True
elif _platform == 'Linux':
    IS_LINUX = True

Phonon = None
try:
    from PyQt4.phonon import Phonon
except ImportError:
    pass

GeoIP2Reader = None
try:
    from geoip2.database import Reader as GeoIP2Reader
except ImportError:
    pass

winsound = None
if IS_WINDOWS:
    try:
        import winsound
    except ImportError:
        pass