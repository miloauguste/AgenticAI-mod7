@echo off
echo Setting up virtual environment and fixing installation issues...

REM Create virtual environment
echo Creating virtual environment...
python -m venv streamlit_env

REM Activate virtual environment
echo Activating virtual environment...
call streamlit_env\Scripts\activate.bat

REM Upgrade pip and build tools
echo Upgrading pip and build tools...
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel build

REM Clear pip cache
echo Clearing pip cache...
pip cache purge

REM Install packages with no-cache-dir to avoid metadata issues
echo Installing packages (this may take a few minutes)...
pip install --no-cache-dir --force-reinstall streamlit
pip install --no-cache-dir plotly
pip install --no-cache-dir pandas
pip install --no-cache-dir python-dotenv

echo Installation complete!
echo.
echo To run the app:
echo 1. Run: streamlit_env\Scripts\activate.bat
echo 2. Then: streamlit run simple_demo.py
echo.
pause