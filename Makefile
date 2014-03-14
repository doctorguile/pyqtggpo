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

.PHONY: all ui qrc clean
all: ui qrc
ui: $(UIPYFILES)
qrc: $(QRCPYFILES)

clean : 
	rm -f $(UIPYFILES) $(UIPYFILES:.py=.pyc) $(QRCPYFILES:.py=.pyc) 
