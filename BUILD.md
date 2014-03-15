# Building on windows

Install python 2.7 32-bit

Install pyqt4 2.7 32-bit

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

	pyinstaller -w -i ggpo/resources/img/icon.ico -n pyqtggpo --runtime-hook ggpo\scripts\runtimehook.py main.py
    copy ggpo\gui\ui\*.* dist\pyqtggpo\ggpo\gui\ui\*.*


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
	yolk -l
	cd pyqtggpo/
	rm -rf dist/pyqtggpo/
	pyinstaller -w -i ggpo/resources/img/icon.icns -n pyqtggpo --runtime-hook ggpo/scripts/runtimehook.py main.py
	deactivate
	./dist/pyqtggpo/pyqtggpo

	du -hs dist/pyqtggpo.app/
	cd dist/
	hdiutil create -srcfolder pyqtggpo.app/ -volname PyQtGGPO -fs HFS+ -fsargs '-c c=64,a=16,e=16' -format UDRW -size 60M PyQtGGPO_tmp.dmg
	hdiutil convert PyQtGGPO_tmp.dmg -format UDZO -imagekey zlib-level=9 -o PyQtGGPO.dmg	
