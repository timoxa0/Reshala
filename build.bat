@echo off

chcp 65001

echo Установка зависимостей
pip install -r req.txt

echo Сборка
pyinstaller.exe -F .\main_gui.py -i icon.ico --collect-all grapheme
if  errorlevel 1 %appdata%\Python\Python311\Scripts\pyinstaller.exe -F .\main_gui.py -i icon.ico --collect-all grapheme
if  errorlevel 1 %localappdata%\Programs\Python\Python311\Scripts\pyinstaller.exe -F .\main_gui.py -i icon.ico --collect-all grapheme
if  errorlevel 1 goto ERROR

cls
echo Сборка завершена!
echo.
echo Логин ОБТ:  learnUser
echo Пароль ОБТ: KoijkfHJEnm49
echo IP ОБТ:     94.103.94.52
echo.
echo Установите Goolgle Chrome, если он не устаовлен
echo Скачать: https://chrome.google.com/
echo.
echo Файл сохранён в папке "dist".
goto EOF

:ERROR
echo Ошибка сборки
goto EOF

:EOF
echo Нажмите любую кнопку для выхода.
pause > nul

