@echo off

:start
echo welcome to Abby's Journal of Neurogenetics citation record generator 
echo Enter a number to select an option
echo 	1. Generate new citation record
echo 	2. Help
echo 	3. Quit
set /p option= Option: 

:options
if %option%==1 (
cls 
call :setup
)
if %option%==2 (
cls
call readme.md
)
if %option%==3 (
exit 
)
else (
echo Please enter a valid option
set /p option= Option: 
call :options
)


pause

call :setup

:setup
:: create venv, install dependencies
echo setting up...
python -m venv newVenv
call newVenv\Scripts\activate
pip3 install tls-client
pip3 install beautifulsoup4
pip3 install typing_extensions
pip3 install openpyxl
pip3 install tqdm
pip3 install matplotlib
pip3 install pyarrow
cls


:data
py getAllArticles.py
echo Getting citations...
py getCitInfo.py
cls
echo Building database...
py makeDatabase.py
cls
echo Analyzing...
py analysis.py


:end
:: delete venv
python deactivate 
rmdir newVenv
echo done :)

pause
