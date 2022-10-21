@echo off

echo Compiling, this might take a few seconds!
pyinstaller --onefile --noconsole -w .\src\main.py -n "SpaceInvaders.exe" --icon=.\resources\gfx\ship.png

echo Cleaning up..

echo Removing SPEC file
del SpaceInvaders.exe.spec

echo Removing BUILD directory
rmdir build /s /q

echo Move exectuable to main directory
MOVE .\dist\SpaceInvaders.exe . >nul

echo Removing DIST directory
rmdir dist
