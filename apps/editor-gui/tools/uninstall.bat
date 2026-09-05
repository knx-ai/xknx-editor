@echo off
setlocal enableextensions
rem XKNX-Editor uninstaller: removes the app from Program Files and the desktop shortcut.
rem Runs from %TEMP% (a staged copy) so it can delete its own install folder while running.

set "DEST=%ProgramFiles%\XKNX-Editor"

rem --- stage a copy in TEMP and re-run from there (can't delete our own folder otherwise) ---
if not "%~1"=="STAGED" (
    copy /Y "%~f0" "%TEMP%\xknx-uninstall.bat" >nul
    start "" "%TEMP%\xknx-uninstall.bat" STAGED
    exit /b
)

rem --- need admin to write/delete under Program Files: re-launch elevated if we are not ---
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Fuer die Deinstallation werden Administratorrechte benoetigt.
    echo Es oeffnet sich eine Nachfrage der Benutzerkontensteuerung ...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -ArgumentList 'STAGED' -Verb RunAs"
    exit /b
)

echo(
echo XKNX-Editor wird deinstalliert von:
echo   "%DEST%"
echo(

rem stop the app if it is running, then remove desktop shortcut(s) and the install directory
taskkill /IM XKNX-Editor.exe /F >nul 2>&1
timeout /t 1 /nobreak >nul
powershell -NoProfile -Command ^
  "Remove-Item ([IO.Path]::Combine([Environment]::GetFolderPath('Desktop'),'XKNX-Editor.lnk')) -ErrorAction SilentlyContinue;" ^
  "Remove-Item ([IO.Path]::Combine([Environment]::GetFolderPath('CommonDesktopDirectory'),'XKNX-Editor.lnk')) -ErrorAction SilentlyContinue"

if exist "%DEST%" rmdir /S /Q "%DEST%"

if exist "%DEST%" (
    echo WARNUNG: "%DEST%" konnte nicht vollstaendig entfernt werden.
    echo Bitte schliessen Sie XKNX-Editor und fuehren Sie die Deinstallation erneut aus.
) else (
    echo Fertig. XKNX-Editor wurde entfernt.
    echo Hinweis: Einstellungen/Cache unter dem Benutzerprofil bleiben erhalten.
)
echo(
endlocal
pause
