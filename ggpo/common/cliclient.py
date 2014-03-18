# -*- coding: utf-8 -*-
from collections import OrderedDict


# noinspection PyClassHasNoInit
class CLI:
    ARG_TYPE, HELPSTRING = range(2)
    NO_ARG, REQUIRED_ARG, OPTIONAL_ARG = range(3)

    commands = OrderedDict([
        ("/away", [NO_ARG, "away from keyboard"]),
        ("/back", [NO_ARG, "become available to play"]),
        ("/accept", [OPTIONAL_ARG, "accept incoming challenge"]),
        ("/decline", [OPTIONAL_ARG, "decline incoming challenge"]),
        ("/challenge", [REQUIRED_ARG, "challenge player"]),
        ("/cancel", [NO_ARG, "cancel outgoing challenge"]),
        ("/watch", [REQUIRED_ARG, "spectate a game"]),
        ("/motd", [NO_ARG, "clear screen and show message of the day"]),
        ("/help", [NO_ARG, "display help menu"])
    ])

    @classmethod
    def helptext(cls):
        def argtext(v):
            return v[cls.ARG_TYPE] == cls.NO_ARG and " " or " [name]"

        return "Available commands:\n" + \
               "\n".join(["{}{}  -   {}".format(k, argtext(v), v[cls.HELPSTRING])
                          for k, v in cls.commands.items()])

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
            controller.sigStatusMessage.emit("Going AFK")
            afkSetChecked(True)
            controller.sendToggleAFK(1)

        def cliback():
            controller.sigStatusMessage.emit("{} is back for more".format(controller.username))
            afkSetChecked(False)
            controller.sendToggleAFK(0)

        def clicancel():
            if controller.challenged:
                controller.sigStatusMessage.emit("Cancelled outgoing challenge to {}".format(controller.challenged))
                controller.sendCancelChallenge(controller.challenged)
            else:
                controller.sigStatusMessage.emit("No outgoing challenge to cancel")

        def clichallenge(name):
            if name in controller.available:
                controller.sigStatusMessage.emit("Challenging {}".format(name))
                controller.sendChallenge(name)
            else:
                controller.sigStatusMessage.emit("{} is not playing".format(name))

        def clidecline(name=None):
            if name:
                controller.sigStatusMessage.emit("Declined {}'s challenge".format(name))
                controller.sendDeclineChallenge(name)
            else:
                for challenger in controller.challengers:
                    controller.sigStatusMessage.emit("Declined {}'s challenge".format(challenger))
                    controller.sendDeclineChallenge(challenger)

        def clihelp():
            controller.sigStatusMessage.emit(cls.helptext())

        def climotd():
            controller.sendMOTDRequest()

        def cliwatch(name):
            if name in controller.playing.keys():
                controller.sendSpectateRequest(name)
            else:
                controller.sigStatusMessage.emit("{} is not playing".format(name))

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

