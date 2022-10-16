# PhoenixWhisper
This is the project for an OpenAI Whisper and GPT/MTM use case: a language learning platform that lets you watch your favorite YouTube videos with two subtitles that run in parallel with the video

Creating a Virtual Environment:
```bash
python -m venv venv

source venv/Scripts/activate (Windows)
```
For this project you need libraries on top of Python:
```bash
pip install --upgrade pytube 

pip install git+https://github.com/openai/whisper.git -q

```

Open web app
```bash
cd webapp

python app.py or flask run
```
