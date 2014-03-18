pyqtggpo
========

This is a cross platform (Linux,  MacOSX, Windows) GUI client for
[GGPO.net](http://ggpo.net/) written in python using the
[pyqt4](http://www.riverbankcomputing.com/software/pyqt/download) framework.

&copy;2014 papasi GPL v2 License

# Features
- Support dark theme to reduce eye strain
- More accurate GeoIP info
- Simple emoticons support
- Autocomplete in chat
- Built in CLI commands in chat, type `/help` to see a list of commands

# Installation

- [Register a ggpo account](http://ggpo.net/forums/ucp.php?mode=register) if needed

- Download and extract the official [ggpo-build-030.zip](http://ggpo.net/ggpo-build-030.zip) GGPO client to a folder. Create a `ROMs` folder inside. You'll need to put the rom zip files in the `ROMs` directory.

- [Open UDP ports 6000-6009 (inbound/outbound) and TCP port 7000 (outbound)](http://portforward.com/english/routers/port_forwarding/routerindex.htm) in your home network

## Windows

1. Download and extract [pyqtggpo.zip](https://github.com/doctorguile/pyqtggpo/releases/)

2. Double click pyqtggpo.exe, login with your ggpo credential

3. Go to `Settings` > `Locate ggpofba.exe` and select the ggpofba.exe file you extracted from the official client.

## Mac
![alt text](http://i.imgur.com/Yas0DOm.png "Wine.app Downloads")

1. Go to "[Wine.app Downloads](http://winebottler.kronenberg.org/downloads)" and scroll to the middle section and download the Wine.app.

2. Run Wine.dmg and drag the wine icon to your Applications folder

3. Run Wine at least once (OSX will ask if you want to run this application downloaded from internet)

4. Download [PyQtGGPO.dmg](https://github.com/doctorguile/pyqtggpo/releases/)

5. Double click PyQtGGPO.dmg to mount it, go to the mounted volume and drag `PyQtGGPO` app to your `Applications` folder

6. Right click PyQtGGPO, select `open` from the context menu. Confirm to run.

7. login with your ggpo credential

8. Go to `Settings` > `Locate ggpofba.exe` and select the ggpofba.exe file you extracted from the official client.


## Linux
Only source code distribution is available currently, you'll need
[wine](http://www.winehq.org/) and
[pyqt4](http://www.riverbankcomputing.com/software/pyqt/download)
for your Linux distribution

To install on Debian based systems (ubuntu, etc), you can type this in a terminal

	sudo apt-get install wine python-qt4-phonon python-qt4 python-pip python-dev build-essential
	sudo pip install geoip2

Download GeoIP2 database [GeoLite2-Country.mmdb.gz](http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz)
and gunzip GeoLite2-Country.mmdb to a folder.

Either download and gunzip [pyqtggpo source tarball](https://github.com/doctorguile/pyqtggpo/tarball/master) or

	sudo apt-get install git
    git clone https://github.com/doctorguile/pyqtggpo.git

1. Make sure you have wine installed

2. Run ```winecfg``` and check the option to "Emulate a virtual desktop"

3. cd pyqtggpo && python main.py

4. Login with your ggpo credential

5. Go to `Settings` > `Locate ggpofba.exe` and select the ggpofba.exe file you extracted from the official client.

6. Go to `Settings` > `Locate GeoIP mmdb` and select the GeoLite2-Country.mmdb file.

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