@echo off
echo Installing CrewAI and dependencies...

REM Activate virtual environment if it exists
if exist streamlit_env\Scripts\activate.bat (
    call streamlit_env\Scripts\activate.bat
)

echo Installing CrewAI...
pip install --no-cache-dir crewai

echo Installing LangGraph...
pip install --no-cache-dir langgraph

echo Installing LangChain components...
pip install --no-cache-dir langchain
pip install --no-cache-dir langchain-openai

echo Installing additional tools...
pip install --no-cache-dir google-search-results
pip install --no-cache-dir tiktoken

echo Done! Testing imports...
python -c "import crewai; print('✅ CrewAI installed successfully')"

pause