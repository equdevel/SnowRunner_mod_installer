@echo off

set ROOT=%CD%\..\..

call %ROOT%\exe\env.cmd SnowRunner

%ROOT%\exe\mod_installer.exe --reinstall --no-pause

echo.
pause