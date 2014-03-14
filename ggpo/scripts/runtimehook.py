# -*- coding: utf-8 -*-
# need to run this first when using pyinstaller
import sip
# Tell qt to return python string instead of QString
# These are only needed for Python v2 but are harmless for Python v3.
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
