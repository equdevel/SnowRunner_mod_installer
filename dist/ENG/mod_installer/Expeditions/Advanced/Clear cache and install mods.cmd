@echo off

set ROOT=%CD%\..\..

call %ROOT%\exe\env.cmd Expeditions

%ROOT%\exe\mod_installer.exe --clear-cache --update --no-pause

echo.
pause