from flask import Flask, redirect, url_for, request, render_template
from pytube import extract, YouTube
import os
import whisper
import json
import datetime
import pathlib
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    file = open('video_list.txt', mode='r')
    video_list = file.read()
    # close the file
    file.close()
    return render_template('form.html', video_list=video_list)


@app.route('/success/<name>/<lan>')
def success(name, lan):
    return render_template('index.html', name=name, lan=lan)


def timedelta_to_videotime(delta):
    """
    Here's a janky way to format a
    datetime.timedelta to match
    the format of vtt timecodes.
    """
    parts = delta.split(":")
    if len(parts[0]) == 1:
        parts[0] = f"0{parts[0]}"
    new_data = ":".join(parts)
    parts2 = new_data.split(".")
    if len(parts2) == 1:
        parts2.append("000")
    elif len(parts2) == 2:
        parts2[1] = parts2[1][:3]
    final_data = ".".join(parts2)
    return final_data


def translate_text(text: str, src_lang: str, target_lang: str, translator: str) -> str:
        # facebook multi lingual translation model
    if translator == 'mtm':
        # get the model and tokenizer
        translator_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
        tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

        # translate
        tokenizer.src_lang = src_lang

        encoded_text = tokenizer(text, return_tensors="pt")
        generated_tokens = translator_model.generate(**encoded_text, forced_bos_token_id=tokenizer.get_lang_id(target_lang))
        translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    
    return translation[0]

def whisper_segments_to_vtt_data(result_segments, src_lan, target_lan):
    """
    This function iterates through all whisper
    segements to format them into WebVTT.
    """
    data = "WEBVTT\n\n"
    for idx, segment in enumerate(result_segments):
        num = idx + 1
        data += f"{num}\n"
        start_ = datetime.timedelta(seconds=segment.get('start'))
        start_ = timedelta_to_videotime(str(start_))
        end_ = datetime.timedelta(seconds=segment.get('end'))
        end_ = timedelta_to_videotime(str(end_))
        data += f"{start_} --> {end_}\n"
        text = segment.get('text').strip()
        translated_text = translate_text(text, src_lan, target_lan, 'mtm')
        data += f"{text}\n({translated_text})\n\n"
    return data


def transcribe_from_link(link, src_lan, target_lan):
    if link != "":
        print("Transcribing...")
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()

        # # check for destination to save file
        destination = './static/resources'

        id = extract.video_id(link)

        # download the file
        out_file = yt.streams.filter(progressive=True, file_extension="mp4").first(
        ).download(output_path=destination, filename=id + ".mp4")

        print(yt.title + " has been downloaded successfully")

        # save the file
        base, ext = os.path.splitext(out_file)
        file_mp4 = base + '.mp4'

        # result of success
        json_file = base + ".vtt"

        # check if file exists
        if not os.path.exists(json_file):
            # if vtt file does not exist, we create it
            model = whisper.load_model("tiny")
            result = model.transcribe(file_mp4)
            json_object = json.dumps(result, indent=4)

            caption_data = whisper_segments_to_vtt_data(result['segments'], src_lan, target_lan)
            file_vtt = base + '.vtt'
            export_file = pathlib.Path(file_vtt)
            export_file.write_text(caption_data)

            # with open(json_file, "w") as outfile:
            # 	outfile.write(json_object)

            with open("video_list.txt", "a") as file_object:
                file_object.write(f"{yt.title}: {link}\n")

        return base


@app.route('/submit', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(request.form)
        url = request.form['url']
        src_lan = request.form['src_lan']
        target_lan = request.form['target_lan']
        id = extract.video_id(url)

        # start transcribe
        base = transcribe_from_link(url, src_lan, target_lan)
        print("Generating trascript DONE...")
        return redirect(url_for('success', name=id, lan=src_lan))


if __name__ == '__main__':
    app.run(debug=True)
