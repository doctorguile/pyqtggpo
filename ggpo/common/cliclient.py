# -*- coding: utf-8 -*-
from collections import OrderedDict


# noinspection PyClassHasNoInit
class CLI:
    ARG_TYPE, HELPSTRING = range(2)
    NO_ARG, REQUIRED_ARG, OPTIONAL_ARG = range(3)

    commands = OrderedDict([
        ("/away", [NO_ARG,  "away from keyboard"]),
        ("/back", [NO_ARG, "become available to play"]),
        ("/accept", [OPTIONAL_ARG, "accept incoming challenge"]),
        ("/decline", [OPTIONAL_ARG, "decline incoming challenge"]),
        ("/challenge", [REQUIRED_ARG, "challenge player"]),
        ("/cancel", [NO_ARG,  "cancel outgoing challenge"]),
        ("/watch", [REQUIRED_ARG,  "spectate a game"]),
        ("/motd", [NO_ARG,  "clear screen and show message of the day"]),
        ("/help", [NO_ARG,  "display help menu"])
    ])

    # need cleaner api for AFK, passing an action is a hack for now
    @classmethod
    def process(cls, controller, afkSetChecked, line):
        def cliaccept(name=None):
            if not name:
                for challenger in controller.challengers:
                    name = challenger
            if name:
                controller.sendAcceptChallenge(name)

        def cliaway():
            afkSetChecked(True)
            controller.sendToggleAFK(1)

        def cliback():
            afkSetChecked(False)
            controller.sendToggleAFK(0)

        def clicancel():
            controller.sendCancelChallenge(controller.challenged)

        def clichallenge(name):
            if name in controller.available:
                controller.sendChallenge(name)

        def clidecline(name=None):
            if name:
                controller.sendDeclineChallenge(name)
            else:
                for challenger in controller.challengers:
                    controller.sendDeclineChallenge(challenger)

        def clihelp():
            msg = "Available commands\n" + \
                  "\n".join([k + (v[cls.ARG_TYPE] == cls.NO_ARG and " " or " [name]") + "  -  " + v[cls.HELPSTRING]
                             for k, v in cls.commands.items()])
            controller.sigStatusMessage.emit(msg)

        def climotd():
            controller.sendMOTDRequest()

        def cliwatch(name):
            if name in controller.playing.keys():
                controller.sendSpectateRequest(name)

        words = line.split(None, 1)
        command = words[0]
        if command in cls.commands:
            cmd = cls.commands[command]
            callback = locals()['cli' + command[1:]]
            if cmd[cls.ARG_TYPE] == cls.NO_ARG:
                callback()
            elif cmd[cls.ARG_TYPE] == cls.REQUIRED_ARG:
                if len(words) != 2:
                    clihelp()
                else:
                    callback(words[1])
            elif cmd[cls.ARG_TYPE] == cls.OPTIONAL_ARG:
                if len(words) >= 2:
                    callback(words[1])
                else:
                    callback()
        else:
            clihelp()

