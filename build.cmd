@echo off

rmdir /s /q build 2> NUL
del mod_installer.spec 2> NUL

call venv313\Scripts\activate

pyinstaller --onefile --noupx --distpath dist\RUS\mod_installer\exe mod_installer.py

copy /y dist\RUS\mod_installer\exe\mod_installer.exe dist\ENG\mod_installer\exe\

call deactivate

pause