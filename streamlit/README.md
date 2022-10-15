# YouTube-transcriber

Creating a Virtual Environment:
command to create virtual env: python -m venv venv
command to start virtual env: source venv/Scripts/activate (Windows)

For this project you need libraries on top of Python:
pip install --upgrade pytube 
pip install youtube_transcript_api
pip install git+https://github.com/openai/whisper.git -q
pip install streamlit

These libraries will enable us to create a front-end for our project, download youtube videos and extract audio files from youtube videos respectively.