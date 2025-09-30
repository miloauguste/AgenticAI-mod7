@echo off
echo Fixing installation issues...

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing build tools...
pip install --upgrade setuptools wheel

echo Installing packages one by one...
pip install streamlit
pip install plotly
pip install pandas
pip install python-dotenv
pip install openai
pip install requests

echo Done! Try running: streamlit run streamlit_app.py
pause