@echo off
echo Fixing SerpAPI installation...

REM Activate virtual environment if it exists
if exist streamlit_env\Scripts\activate.bat (
    call streamlit_env\Scripts\activate.bat
)

echo Uninstalling any existing SerpAPI packages...
pip uninstall -y serpapi google-search-results

echo Installing correct SerpAPI package...
pip install --no-cache-dir google-search-results

echo Testing SerpAPI import...
python -c "from serpapi.google_search_results import GoogleSearchResults; print('✅ SerpAPI import successful')"

pause