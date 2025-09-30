@echo off
echo Installing required packages...

pip install streamlit==1.29.0
pip install plotly==5.17.0
pip install pandas==2.1.4
pip install networkx==3.2.1
pip install crewai==0.28.8
pip install langgraph==0.0.32
pip install langchain==0.1.0
pip install langchain-openai==0.0.8
pip install openai==1.12.0
pip install google-search-results==2.4.2
pip install python-dotenv==1.0.0
pip install tiktoken==0.5.2

echo Installation complete!
pause