@echo off

set ROOT=%CD%\..\..

call %ROOT%\exe\env.cmd SnowRunner

set /p MOD_ID=<MOD_ID.txt

%ROOT%\exe\mod_installer.exe --reinstall %MOD_ID% --no-pause

echo.
pause