# Phoenix Whisper

### About
This is the project using OpenAI Whisper with GPT/MTM language model to create a language learning platform that lets you watch your favorite YouTube videos with dual interactive transcripts

![Home page](home_page.png)
![App Interface](transcript.png)

## User Guide
<b> There are two options to translate your favorite YouTube video, either way, you need a valid YouTube URL and [a language code](https://www.andiamo.co.uk/resources/iso-language-codes/) that you want the translation, then if you </b>
1. Use OpenAI GPT if you have an API key
  - Choose GPT as the translation model
  - Enter your API key, you can get one from your dashboard
  - The "Initial Prompt" is the translation of "Today is a beautiful day" in the language that you chose above. For example, if I choose "vi" (which stands for Vietnamese), I need to write "Hôm nay trời đẹp quá" as the answer (the translation of "Today is a beautiful day" in Vietnamese) for this section
2. Using Meta's language model MTM
  - Just click submit/enter after you fill out the URL and the language code and you're done! :)

## Installation

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

