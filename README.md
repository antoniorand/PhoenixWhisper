# Phoenix Whisper
This is the project for an OpenAI Whisper with GPT/MTM use case: a language learning platform that lets you watch your favorite YouTube videos with dual subtitles

![Home page](home_page.png)
![App Interface](transcript.png)

Creating virtual environment:
```bash
cd webapp

python -m venv venv

source venv/Scripts/activate (Windows)
```
For this project you need libraries on top of Python:
```bash
pip install --upgrade pytube 

pip install git+https://github.com/openai/whisper.git -q

pip install flask openai sentencepiece
```

Running web app
```bash
python app.py or flask run
```
