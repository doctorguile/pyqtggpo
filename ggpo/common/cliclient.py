# -*- coding: utf-8 -*-
import sip
# Tell qt to return python string instead of QString
# These are only needed for Python v2 but are harmless for Python v3.
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
import threading
from playerstate import PlayerStates
from controller import Controller


def chatResponse(name, msg):
    print "<" + name + "> " + msg


def bailoutCallback(msg):
    def bailout():
        print msg
        sys.exit()

    return bailout


def msgCallback(msg=''):
    def printmsg(*args):
        if args:
            print msg + ' '.join(args)
        else:
            print msg

    return printmsg


def playerStateChange(name, state):
    if state == PlayerStates.QUIT:
        print '-!- ' + name + " left"
    elif state == PlayerStates.AVAILABLE:
        print '-!- ' + name + " becomes available"
    elif state == PlayerStates.AFK:
        print '-!- ' + name + " is away from keyboard"
    elif state == PlayerStates.PLAYING:
        print '-!- ' + name + " started a game"


def cliclient(argv):
    # thread = QtCore.QThread()
    g = Controller()

    if not g.connectTcp():
        sys.exit()
    g.connectUdp()

    def refreshUsers():
        print "-!- Player list"
        for p in g.available.keys():
            print p
        for p in g.awayfromkb.keys():
            print p + ' (AFK)'
        for p, p2 in g.playing.items():
            print p + ' vs ' + p2

    def loadRooms():
        keys = sorted(g.channels.keys())
        for k in keys:
            print k + ' - ' + g.channels[k]['title']

    def readlineLoop():
        commands = {
            "/challenge": g.sendChallenge,
            "/cancel": g.sendCancelChallenge,
            "/accept": g.sendAcceptChallenge,
            "/decline": g.sendDeclineChallenge,
            "/watch": g.sendSpectateRequest,
            "/join": g.sendJoinChannelRequest,
            "/list": g.sendListChannels,
            "/users": g.sendListUsers,
            "/motd": g.sendMOTDRequest,
            "/away": lambda: g.sendToggleAFK(1),
            "/afk": lambda: g.sendToggleAFK(1),
            "/back": lambda: g.sendToggleAFK(0),
            "/exit": sys.exit,
            "/quit": sys.exit,
        }
        commandsReqArg = ["challenge", "cancel", "accept", "decline", "watch", "join"]

        while True:
            line = sys.stdin.readline().strip()
            if not line:
                continue
            words = line.split(None, 1)
            cmd = words[0]
            if cmd in commands:
                cb = commands[cmd]
                if cmd[1:] in commandsReqArg:
                    if len(words) == 2:
                        cb(words[1])
                else:
                    cb()
            else:
                if line.startswith('/'):
                    print "Available commands\n"
                    print "\n".join(sorted(commands.keys()))
                else:
                    g.sendChat(line)

    g.sigServerDisconnected.connect(bailoutCallback('-!- Disconnected from server'))
    g.sigLoginSuccess.connect(msgCallback('-!- Logged In'))
    g.sigLoginFailed.connect(bailoutCallback('-!- Invalid username / password'))
    g.sigActionFailed.connect(msgCallback('-!- Failed - '))
    g.sigStatusMessage.connect(msgCallback('-!- '))
    g.sigChallengeDeclined.connect(msgCallback('-!- Challege declined by '))
    g.sigChallengeCancelled.connect(msgCallback('-!- Challege cancelled by '))
    g.sigChallengeReceived.connect(msgCallback('-!- Challege sent by '))
    g.sigMotdReceived.connect(msgCallback('-!- Message of the day - '))
    g.sigPlayerStateChange.connect(playerStateChange)
    g.sigChatReceived.connect(chatResponse)
    g.sigPlayersLoaded.connect(refreshUsers)
    g.sigChannelsLoaded.connect(loadRooms)

    t = threading.Thread(target=g.selectLoop)
    t.daemon = True
    t.start()

    g.sendWelcome()
    g.sendAuth(argv[1], argv[2])
    readlineLoop()


if __name__ == '__main__':
    import sys

    print(sys.argv[0])
    cliclient(sys.argv)