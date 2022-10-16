from flask import Flask, redirect, url_for, request, render_template
from pytube import extract, YouTube
import os, whisper, json
import datetime
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import openai

app = Flask(__name__)
lang_dict = {'en': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish', 'vi': 'Vietnamese', 'sv': 'Swedish'}

# set file path
webapp_path = os.path.dirname(os.path.realpath(__file__))

# get the model and tokenizer
translator_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")


@app.route('/', methods=['GET'])
def home():
    with open(os.path.join(webapp_path, 'video_list.txt'),mode='r') as file:
        video_list = file.read()
    return render_template('form.html', video_list=video_list)
 

@app.route('/success/<name>/<target_lan>')
def success(name, target_lan):
    return render_template('index.html', name=name, target_lan=target_lan)


def timedelta_to_videotime(delta):
    """
    Format datetime.timedelta to match the format of vtt time 
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

def translate_text(output, target_lan = "es", translation_model = "mtm", openai_apikey="", initial_prompt="") -> str:
    if translation_model == "" or translation_model == 'mtm':
        # translate 
        tokenizer.src_lang = output["language"]

        # loop through transcription and translate
        for k, item in enumerate(output['segments']):
            src_text = item['text']

            encoded_text = tokenizer(src_text, return_tensors="pt")
            generated_tokens = translator_model.generate(**encoded_text, forced_bos_token_id=tokenizer.get_lang_id(target_lan))
            tgt_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

            output['segments'][k]["text"] += f" ({tgt_text[0]})"
            output['segments'][k]["tokens"] = []
            # print(output['segments'][k]["text"])

    if translation_model == 'gpt' and openai_apikey != "":
        openai.api_key = openai_apikey
        src_lang = output["language"]

        src_language = "en"
        target_language = "es"

        if src_lang in lang_dict:
            src_language = lang_dict[src_lang]
        
        if target_lan in lang_dict:
            target_language = lang_dict[target_lan]

        # prompt
        prompt_base = 'Translate '+ src_language +' to '+ target_language + f': \n\n Todays is a beautiful day => {initial_prompt} \n\n '
        
        # loop through transcription and translate
        for k, item in enumerate(output['segments']):
            text = item['text']

            # append text to prompt
            prompt = prompt_base + text + " => "

            # Note: rule of thumb to avoid random continuation
            max_tokens = 6*len(text.split())

            response = openai.Completion.create(
                model="text-curie-001", # text-davinci-002 -> bigger model for later
                prompt=prompt,
                temperature=0.1,
                max_tokens=max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            output['segments'][k]["text"] += f" ({response['choices'][0]['text']})"
            output['segments'][k]["tokens"] = []

            # print(output['segments'][k]["text"])
    
    return output['segments']


def whisper_segments_to_vtt_data(result_segments):
  """
  This function iterates through all whisper
  segements to format them into WebVTT.
  """
  data = "WEBVTT\n\n"
  for idx, segment in enumerate(result_segments):
    num = idx + 1
    data+= f"{num}\n"
    start_ = datetime.timedelta(seconds=segment.get('start'))
    start_ = timedelta_to_videotime(str(start_))
    end_ = datetime.timedelta(seconds=segment.get('end'))
    end_ = timedelta_to_videotime(str(end_))
    data += f"{start_} --> {end_}\n"
    text = segment.get('text').strip()
    data += f"{text}\n\n"
  return data


def transcribe_from_link(link, target_lan, openai_apikey, translation_model, initial_prompt):
    if link != "":
        print("Transcribing...")	
        yt = YouTube(link)
        yt.streams.filter(only_audio=True).first()
        
        # # check for destination to save file
        destination = os.path.join(webapp_path, 'static', 'resources')
        id = extract.video_id(link)
        
        # download the file
        out_file = yt.streams.filter(progressive = True, file_extension = "mp4").first().download(output_path=destination, filename = id + ".mp4")

        print(yt.title + " has been downloaded successfully")

        # save the file
        base, ext = os.path.splitext(out_file)
        file_mp4 = base + '.mp4'

        # result of success
        lan_file = base + f".{target_lan}.vtt"
        vtt_file = base + ".vtt"
        json_file = base + ".json"

        # check if file exists
        if not os.path.exists(lan_file):
            if not os.path.exists(json_file):
                # if vtt file does not exist, we create it
                model = whisper.load_model("tiny")
                result = model.transcribe(file_mp4)

                # Save original caption_data
                caption_data = whisper_segments_to_vtt_data(result['segments'])
                file_vtt = base + '.vtt'
                with open(file_vtt, "w", encoding='utf-8') as outfile:
                    outfile.write(caption_data)
                
                # save the caption for the original language
                with open(base + f'.{result["language"]}.vtt', "w", encoding='utf-8') as outfile:
                    outfile.write(caption_data)

                print(yt.title + ": Transcript has been successfully generated")

                json_object = json.dumps(result, indent=4)
                with open(json_file, "w", encoding="utf-8") as outfile:
                    outfile.write(json_object)
                    
                with open(os.path.join(webapp_path, "video_list.txt"), "a") as file_object:
                    file_object.write(f"{yt.title}: {link}\n")

                if result["language"] != target_lan: # check if original language is different from target language
                    output = translate_text(output=result, target_lan=target_lan, openai_apikey=openai_apikey, translation_model=translation_model, initial_prompt=initial_prompt)

                    # Save translation file_vtt
                    caption_data = whisper_segments_to_vtt_data(output)
                    translate_vtt = base + f'.{target_lan}.vtt'
                    with open(translate_vtt, "w", encoding='utf-8') as outfile:
                        outfile.write(caption_data)

            else: 
                # read json file and generate translated caption
                f = open(json_file)
                data = json.load(f)   
                output = translate_text(output=data, target_lan=target_lan, openai_apikey=openai_apikey, translation_model=translation_model, initial_prompt=initial_prompt)

                # Save translation file_vtt
                caption_data = whisper_segments_to_vtt_data(output)
                translate_vtt = base + f'.{target_lan}.vtt'
                with open(translate_vtt, "w", encoding='utf-8') as outfile:
                    outfile.write(caption_data)
                    
        return base
 

@app.route('/submit', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(request.form)
        url = request.form['url']
        target_lan = request.form['target_lan']
        openai_apikey = request.form['openai_apikey']
        translation_model = request.form['translation_model']
        initial_prompt = request.form['initial_prompt']
        id=extract.video_id(url)

        # start transcribe
        base = transcribe_from_link(link=url, target_lan=target_lan, openai_apikey=openai_apikey, translation_model=translation_model, initial_prompt=initial_prompt)
        print(f"Generating trascript DONE at {base}")
        return redirect(url_for('success', name=id, target_lan=target_lan))


if __name__ == '__main__':
    app.run(debug=True)