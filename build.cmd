@echo off

rmdir /s /q build
del mod_installer.spec

call venv313\Scripts\activate

pyinstaller --onefile --noupx --distpath dist\RUS\mod_installer\exe mod_installer.py

copy /y dist\RUS\mod_installer\exe\mod_installer.exe dist\ENG\mod_installer\exe\

call deactivate

pause