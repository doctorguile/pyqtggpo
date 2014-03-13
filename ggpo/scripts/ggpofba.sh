#!/bin/sh

# ggpofba wrapper script for version 0.2.96.74 (bundled with ggpo)
# (c)2013-2014 Pau Oliva Fora (@pof)
# (c)2014 papasi

# This resets pulseaudio on Linux because otherwise FBA hangs on my computer (WTF!?).
# For best results run 'winecfg' and check the option to "Emulate a virtual desktop"
# under the Graphics tab. I've it set to 1152x672 for best full screen aspect ratio.

WINE="$1"
shift
FBA="$1"
shift

if [ ! -x ${WINE} ] || [ ! -e ${FBA} ]; then
	exit 1
fi

if [ ! -x /usr/bin/pulseaudio ] || [ ! -x /usr/bin/pacmd ] || [ ! -x /usr/bin/pactl ]; then
    ${WINE} ${FBA} ${1+"$@"} &
	exit 0
fi

# check if there are multiple instances running
tot=$(ps ax |grep ggpofba.exe |grep quark |wc -l)

# first instance resets pulseaudio, others don't
if [ ${tot} -eq 0 ]; then
    VOL=$(/usr/bin/pacmd dump |grep "^set-sink-volume" |tail -n 1 |awk '{print $3}')
    echo "-!- resetting pulseaudio"
    /usr/bin/pulseaudio -k
    /usr/bin/pulseaudio --start
fi

echo "-!- starting the real ggpofba"
${WINE} ${FBA} ${1+"$@"} &

if [ ${tot} -eq 0 ]; then
    sleep 1s
    echo "-!- restoring volume value"
    /usr/bin/pactl set-sink-volume 0 ${VOL}
fi