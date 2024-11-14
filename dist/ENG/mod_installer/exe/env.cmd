@echo off

set GAME=%1

for /f "usebackq delims=" %%i in (`powershell -Command "[Environment]::GetFolderPath('MyDocuments')"`) do set MY_DOCS=%%i

set MODS_DIR=%MY_DOCS%\My Games\%GAME%\base\Mods\.modio\mods

rem set /p USER_PROFILE=<%ROOT%\%GAME%\PROFILE.txt
if %GAME%==SnowRunner (set S_FLAG=1) else if %GAME%==Expeditions (set S_FLAG=0)
set S_COND=Where-Object {(Get-ChildItem -Path $_.Directory.FullName -File -Filter 'GameVersionSave.*').Count -eq %S_FLAG%}
for /f "usebackq delims=" %%i in (`powershell -Command "(Get-ChildItem -Path '%MY_DOCS%\My Games\%GAME%\base\storage', '%PUBLIC%\Documents\Steam' -Recurse -Exclude 'backupSlots' -File -Filter 'user_profile.*' | %S_COND% | Sort-Object -Property LastAccessTimeUtc -Descending | Select-Object -First 1).FullName"`) do set USER_PROFILE=%%i

for /f "usebackq delims=" %%i in (`powershell -Command "Get-Content '%ROOT%\TOKEN.txt' -Raw"`) do set ACCESS_TOKEN=%%i