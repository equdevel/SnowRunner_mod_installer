@echo off

rmdir /s /q build 2> NUL
del *.spec 2> NUL
del *.c 2> NUL
del *.pyd 2> NUL
del *.html 2> NUL

call venv313\Scripts\activate

python cython_setup.py build_ext --inplace

pyinstaller --onefile --noupx --noconfirm --clean --distpath dist\RUS\mod_installer\exe --name mod_installer mod_installer_cython.py

copy /y dist\RUS\mod_installer\exe\mod_installer.exe dist\ENG\mod_installer\exe\

call deactivate

pause