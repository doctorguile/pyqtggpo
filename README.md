pyqtggpo
========

This is a cross platform (Linux,  MacOSX, Windows) GUI client for
[GGPO.net](http://ggpo.net/) written in python using the
[pyqt4](http://www.riverbankcomputing.com/software/pyqt/download) framework.

&copy;2014 papasi<br />
GPL v2 License 

## Features
Support dark theme to reduce eye strain
Autocomplete in chat
More accurate GeoIP info
Simple emoticons support

## Installation
Click the [Download ZIP](https://github.com/doctorguile/pyqtggpo/archive/master.zip) button at right and extract it to a folder.

Download and extract the official [ggpo-build-030.zip](http://ggpo.net/ggpo-build-030.zip) GGPO client to another folder.

### Linux
1. Make sure you have [wine](http://www.winehq.org/) and
[pyqt4](http://www.riverbankcomputing.com/software/pyqt/download) installed 
on your Linux distribution

2. Run ```winecfg``` and check the option to "Emulate a virtual desktop"

To install on Debian based systems (ubuntu, etc), you can type this in a terminal

	sudo apt-get install wine python-qt4

Optional (for playing the challenger sound and better geo location support of players)

	sudo apt-get install python-qt4-phonon python-pip python-dev build-essential 
	sudo pip install geoip2


### Mac
![alt text](http://i.imgur.com/Yas0DOm.png "Wine.app Downloads")

1. Go to "[Wine.app Downloads](http://winebottler.kronenberg.org/downloads)" and scroll to the middle section and download the Wine.app.

2. Run Wine.dmg and drag the wine icon to your Applications folder

3. Run Wine at least once (OSX will ask if you want to run this application downloaded from internet)

4. Install pyqt4

Easiest method with [Homebrew](http://brew.sh/)

    ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
    brew install qt
    brew install sip
    brew install pyqt
    sudo easy_install pip
    pip install geoip2

### Windows
Determine if your windows is 64 or 32-bit. 

1. Download and install [python 2.7.x for windows](http://python.org/download/releases/2.7.6/)
2. Download and install [PyQt4-gpl-Py2.7-Qt4.8](http://www.riverbankcomputing.com/software/pyqt/download).

## Usage
[Register a ggpo account](http://ggpo.net/forums/ucp.php?mode=register) if needed

Execute ```python main.py```

Login with your ggpo credential

Go to `Settings` => `Locate ggpofba.exe` and select the ggpofba.exe file you extracted from the official client.

If you have GeoIP2 module installed, download
[GeoLite2-Country.mmdb.gz](http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz)
and extract GeoLite2-Country.mmdb to a folder.
Go to `Settings` => `Locate GeoIP mmdb` and select the GeoLite2-Country.mmdb file you extracted.
This will allow you to see the missing geoip info from the official ggpo client.

## Credits
Tony Cannon (Ponder) Tom Cannon (ProtomCannon)<br />
For the original [ggpo client](http://ggpo.net), innovative p2p
protocol and hosting the service for free

Pau Oliva Fora (@pof)<br />
For the amazing job of reverse engineering the client protocol
and the [CLI client](http://poliva.github.io/ggpo/) that provides
most of the ground work for this GUI port, as well as the wine installation instructions.

## Screenshots
![alt text](http://i.imgur.com/E80zA9t.png "ggpo screenshot 0")
![alt text](http://i.imgur.com/ofh4mwQ.png "ggpo screenshot 1")

