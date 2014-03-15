PYUIC = pyuic4
PYRCC = pyrcc4

UIFILES := $(wildcard ggpo/gui/ui/*.ui)
UIPYFILES := $(UIFILES:.ui=_ui.py)
QRCFILES := $(wildcard ggpo/resources/*.qrc)
QRCPYFILES := $(QRCFILES:.qrc=_rc.py)

%_ui.py: %.ui
	$(PYUIC) $< --output $@

%_rc.py : %.qrc
	$(PYRCC) $< -o $@

.PHONY: all ui qrc clean osxapp osxdmg osxclean
all: ui qrc
ui: $(UIPYFILES)
qrc: $(QRCPYFILES)

clean:
	rm -f $(UIPYFILES) $(UIPYFILES:.py=.pyc) $(QRCPYFILES:.py=.pyc) 

osxapp:
	pyinstaller -w -i ggpo/resources/img/icon.icns -n PyQtGGPO --runtime-hook ggpo/scripts/runtimehook.py main.py

osxdmg:
	cd dist; \
	hdiutil create -srcfolder PyQtGGPO.app -volname PyQtGGPO -fs HFS+ -fsargs '-c c=64,a=16,e=16' -format UDRW -size 60M PyQtGGPO_tmp.dmg; \
	hdiutil convert PyQtGGPO_tmp.dmg -format UDZO -imagekey zlib-level=9 -o PyQtGGPO.dmg ; \
	rm -f PyQtGGPO_tmp.dmg

osxclean:
	rm -rf dist