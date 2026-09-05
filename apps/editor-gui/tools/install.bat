@echo off
setlocal enableextensions
rem XKNX-Editor installer: copies this folder to Program Files, creates a desktop shortcut,
rem and starts the app once. Run it from the extracted "XKNX-Editor" folder (double-click).

rem --- need admin to write to Program Files: re-launch elevated if we are not ---
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Fuer die Installation nach Program Files werden Administratorrechte benoetigt.
    echo Es oeffnet sich eine Nachfrage der Benutzerkontensteuerung ...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

set "SRC=%~dp0"
set "DEST=%ProgramFiles%\XKNX-Editor"
set "EXE=%DEST%\XKNX-Editor.exe"

echo(
echo XKNX-Editor wird installiert nach:
echo   "%DEST%"
echo(

if not exist "%DEST%" mkdir "%DEST%"
rem robocopy: copy everything except this installer; exit codes 0-7 mean success.
robocopy "%SRC%." "%DEST%" /E /NFL /NDL /NJH /NJS /NC /NS /XF install.bat >nul
if %errorlevel% geq 8 (
    echo FEHLER beim Kopieren der Dateien. Installation abgebrochen.
    pause
    exit /b 1
)

rem Remove the "Mark of the Web" from the installed files so the installed app and shortcut launch
rem without a Defender SmartScreen prompt (only the downloaded installer itself still warns once).
echo Entferne Download-Markierung (Mark of the Web) ...
powershell -NoProfile -Command "Get-ChildItem -LiteralPath '%DEST%' -Recurse -File | Unblock-File"

echo Erstelle Desktop-Verknuepfung ...
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$lnk = $ws.CreateShortcut([IO.Path]::Combine([Environment]::GetFolderPath('Desktop'),'XKNX-Editor.lnk'));" ^
  "$lnk.TargetPath = '%EXE%';" ^
  "$lnk.WorkingDirectory = '%DEST%';" ^
  "$lnk.IconLocation = '%EXE%';" ^
  "$lnk.Save()"

echo(
echo Fertig. XKNX-Editor wurde installiert und eine Verknuepfung auf dem Desktop angelegt.
echo Diesen entpackten Ordner koennen Sie jetzt loeschen.
echo(
echo Starte XKNX-Editor ...
start "" "%EXE%"

endlocal
pause
