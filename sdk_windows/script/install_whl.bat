@echo off
setlocal

REM Activate the neutorch environment
echo Activating the neutorch environment...
call conda activate neutorch || (
    echo ERROR: Failed to activate neutorch environment.
    exit /b 1
)

REM Run Python script to generate requirements and check for errors
echo Generating pip requirements...
python gen_requires.py win || (
    echo ERROR: Failed to run gen_requires.py.
    exit /b 1
)

REM Install packages from requirements.txt and check for errors
echo Installing packages...
pip3 install --force-reinstall --no-index -r requirements.txt || (
    echo ERROR: Failed to install dependencies from requirements.txt.
    exit /b 1
)

del requirements.txt || (
    echo ERROR: Failed to remove requirements.txt.
    exit /b 1
)

REM Confirm success if all commands succeeded
echo Installation succeeded!

endlocal
