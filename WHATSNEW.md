#Version 0.01
Initial alpha source code release
- Support dark theme to reduce eye strain
- Autocomplete in chat
- More accurate GeoIP info
- Simple emoticons support

#Version 0.02
- Packaged app bundle for OSX and windows

#Version 0.03
- Support a database of ggpo unsupported game save states in the `Unsupported Games` room
- Keyboard shortcuts for resizing splitter
- Embedded command line interface as chat commands<br/>
Type `/help` to see a list of commands available

    /away - away from keyboard
    /back - become available to play
    /accept [name] - accept incoming challenge
    /decline [name] - decline incoming challenge
    /challenge [name] - challenge player
    /cancel - cancel outgoing challenge
    /watch [name] - spectate a game
    /ignore [name] - ignore a player
    /unignore [name] - unignore a player
    /motd - clear screen and show message of the day
    /help - display help menu

## Fixes
- fixes send / receive challenge in 3s and kof rooms
- disable login button while waiting for response from ggpo.net