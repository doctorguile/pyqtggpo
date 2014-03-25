rd /s /q dist
rd /s /q build
pyinstaller -w -i ggpo\resources\img\icon.ico -n pyqtggpo --runtime-hook ggpo\scripts\runtimehook.py main.py
copy "%HOMEPATH%\Downloads\GeoLite2-Country.mmdb" dist\pyqtggpo
del pyqtggpo.zip
cd dist
python ..\ggpo\scripts\zip.py ..\pyqtggpo.zip pyqtggpo
cd ..