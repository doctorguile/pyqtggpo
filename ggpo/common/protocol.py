# -*- coding: utf-8 -*-
import struct


# noinspection PyClassHasNoInit
class Protocol:
    # IN BAND
    WELCOME = 0x0
    AUTH = 0x1
    MOTD = 0x2
    LIST_CHANNELS = 0x3
    LIST_USERS = 0x4
    JOIN_CHANNEL = 0x5
    TOGGLE_AFK = 0x6
    CHAT = 0x7
    SEND_CHALLENGE = 0x8
    ACCEPT_CHALLENGE = 0x9
    DECLINE_CHALLENGE = 0xa
    SPECTATE = 0x10
    CANCEL_CHALLENGE = 0x1c
    # OUT OF BAND
    CHALLENGE_RETRACTED = 0xffffffef
    SPECTATE_GRANTED = 0xfffffffa
    CHALLENGE_DECLINED = 0xfffffffb
    CHALLENGE_RECEIVED = 0xfffffffc
    PLAYER_STATE_CHANGE = 0xfffffffd
    CHAT_DATA = 0xfffffffe
    JOINING_A_CHANNEL = 0xffffffff

    AllReverseMap = {
        0x0: 'WELCOME',
        0x1: 'AUTH',
        0x2: 'MOTD',
        0x3: 'LIST_CHANNELS',
        0x4: 'LIST_USERS',
        0x5: 'JOIN_CHANNEL',
        0x6: 'TOGGLE_AFK',
        0x7: 'CHAT',
        0x8: 'SEND_CHALLENGE',
        0x9: 'ACCEPT_CHALLENGE',
        0xa: 'DECLINE_CHALLENGE',
        0x10: 'SPECTATE',
        0x1c: 'CANCEL_CHALLENGE',
        0xffffffef: 'CHALLENGE_RETRACTED',
        0xfffffffa: 'SPECTATE_GRANTED',
        0xfffffffb: 'CHALLENGE_DECLINED',
        0xfffffffc: 'CHALLENGE_RECEIVED',
        0xfffffffd: 'PLAYER_STATE_CHANGE',
        0xfffffffe: 'CHAT_DATA',
        0xffffffff: 'JOINING_A_CHANNEL',
    }

    OutOfBandReverseMap = {
        0xffffffef: 'CHALLENGE_RETRACTED',
        0xfffffffa: 'SPECTATE_GRANTED',
        0xfffffffb: 'CHALLENGE_DECLINED',
        0xfffffffc: 'CHALLENGE_RECEIVED',
        0xfffffffd: 'PLAYER_STATE_CHANGE',
        0xfffffffe: 'CHAT_DATA',
        0xffffffff: 'JOINING_A_CHANNEL',
    }

    @staticmethod
    def codeToString(code):
        if code in Protocol.AllReverseMap:
            return Protocol.AllReverseMap[code]
        return 'SEQ (' + hex(code) + ')'

    @staticmethod
    def outOfBandCodeToString(code):
        if code in Protocol.OutOfBandReverseMap:
            return Protocol.OutOfBandReverseMap[code]
        return 'SEQ (' + hex(code) + ')'

    @staticmethod
    def unpackInt(data):
        n, = struct.unpack("!I", data)
        return n

    @staticmethod
    def packInt(n):
        return struct.pack("!I", n)

    @staticmethod
    def packTLV(data):
        return struct.pack("!I", len(data)) + data

    @staticmethod
    def extractTLV(data):
        """
        data is encoded in array of bytes in [length:value:rest] format
        extract and return the value and the rest of the bytes in a tuple
        @param data:
        @return: tuple(data, rest)
        """
        length = Protocol.unpackInt(data[:4])
        value = data[4:length + 4]
        return value, data[length + 4:]

    @staticmethod
    def extractInt(data):
        """
        data is encoded in array of bytes in [int32:rest] format
        extract and return the int32 and the rest of the bytes in a tuple
        @param data:
        @return: tuple(int, rest)
        """
        intval = Protocol.unpackInt(data[0:4])
        return intval, data[4:]
