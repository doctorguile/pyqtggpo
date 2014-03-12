# -*- coding: utf-8 -*-
import os.path

import PyQt4.uic

__all__ = ['loadUi']


def loadUi(modpath, widget):
    """
    Uses the PyQt4.uic.loadUI method to load the inputed ui file associated
    with the given module path and widget class information on the inputed
    widget.

    :param      modpath | str
    :param      widget  | QWidget
    """
    # generate the uifile path
    basepath = os.path.dirname(modpath)
    basename = widget.__class__.__name__.lower()
    uifile = os.path.join(basepath, 'ui/%s.ui' % basename)

    # load the ui
    PyQt4.uic.loadUi(uifile, widget)
