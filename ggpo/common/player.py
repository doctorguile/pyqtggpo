# -*- coding: utf-8 -*-
class Player:
    _ID = 0

    def __init__(self, **kwargs):
        self.id = self._ID
        self.__class__._ID += 1
        self.player = ''
        self.ip = ''
        self.port = 6009
        self.city = ''
        self.cc = ''
        self.country = ''
        self.ping = ''
        self.lastPingTime = 0
        self.loc = ''
        vars(self).update(kwargs)