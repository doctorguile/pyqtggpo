# Building on windows

Determine if your windows is 64 or 32-bit.

Download and install [python 2.7.x for windows](http://python.org/download/releases/2.7.6/)

Download and install [PyQt4-gpl-Py2.7-Qt4.8](http://www.riverbankcomputing.com/software/pyqt/download).

Download and install [pywin32](http://sourceforge.net/projects/pywin32/)

##Install setuptools

http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools

##Install pip

http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip

http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools

##Setup PATH

    c:\python2.7
    c:\python2.7\scripts

##Install geoip2

pip install geoip2

##Install pyinstaller from source

https://pypi.python.org/packages/source/P/PyInstaller/PyInstaller-2.1.zip

    python setup.py install

##Build with pyinstaller

	pyinstaller -w -i ggpo\resources\img\icon.ico -n pyqtggpo --runtime-hook ggpo\scripts\runtimehook.py main.py
	copy %HOMEPATH%\Downloads\GeoLite2-Country.mmdb dist\pyqtggpo


# Building on OSX

	sudo port selfupdate
	sudo port install python27
	sudo port install python_select
	port select --list python
	sudo port select --set python python27
	sudo port install phonon
	sudo port install qt-mac
	sudo port install py27-pyqt4

 	sudo port clean py27-pyqt4
 	sudo port clean qt4-mac
 	sudo port selfupdate
 	sudo port install qt4-mac
 	sudo port install py27-pyqt4 +phonon

	sudo port install py27-setuptools py27-virtualenv
	virtualenv-2.7 --system-site-packages ve27
	source ve27/bin/activate
	pip install yolk
	pip install PyInstaller
	pip install geoip2
	cd pyqtggpo/
	rm -rf dist
	pyinstaller -w -i ggpo/resources/img/icon.icns -n pyqtggpo --runtime-hook ggpo/scripts/runtimehook.py main.py
	cp ~/Downloads/GeoLite2-Country.mmdb ./dist/PyQtGGPO.app/Contents/MacOS/
	du -hs dist/pyqtggpo.app/
	cd dist/
	hdiutil create -srcfolder pyqtggpo.app/ -volname PyQtGGPO -fs HFS+ -fsargs '-c c=64,a=16,e=16' -format UDRW -size 60M PyQtGGPO_tmp.dmg
	hdiutil convert PyQtGGPO_tmp.dmg -format UDZO -imagekey zlib-level=9 -o PyQtGGPO.dmg	
