@echo off

echo Installing all dependencies
pip install -r req.txt

echo Building project
%appdata%\Python\Python311\Scripts\pyinstaller.exe -F .\main_gui.py -i icon.ico --collect-all grapheme

cls
echo Build finished!
echo.
echo Your OBT login:    learnUser
echo Your OBT password: KoijkfHJEnm49
echo Your OBT IP:       94.103.94.52
echo.
echo Please install Google Chrome on your PC if one not installed
echo Download link: https://chrome.google.com/
echo.
echo File saved in "dist" directory.
echo Press any key to exit
pause > nul