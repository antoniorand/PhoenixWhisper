from flask import Flask, redirect, url_for, request, render_template
from pytube import extract, YouTube
import os, whisper, json
import datetime
import pathlib
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
# import openai

#this is a comment

app = Flask(__name__)
lang_dict = {'en': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish'}

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

def translate_text(output, target_lan = "es", translation_model = "mtm", openai_apikey="") -> str:
    if translation_model == 'mtm':
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

    # if translation_model == 'gpt' and openai_apikey != "":
    #     openai.api_key = openai_apikey
    #     src_lang = output["language"]
    #     # prompt
    #     prompt_base = 'Translate '+lang_dict[src_lang]+' to '+ lang_dict[target_lan]+ ': \n\n Todays is a beautiful day => Heute ist ein schöner Tag \n\n '
    #     # append text to prompt
    #     prompt = prompt_base + text + " => "

    #     # Note: rule of thumb to avoid random continuation
    #     max_tokens = 6*len(text.split())

    #     response = openai.Completion.create(
    #     model="text-curie-001", # text-davinci-002 -> bigger model for later
    #     prompt=prompt,
    #     temperature=0.1,
    #     max_tokens=max_tokens,
    #     top_p=1.0,
    #     frequency_penalty=0.0,
    #     presence_penalty=0.0
    #     )
    #     translation = response['choices'][0]['text']
    
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


def transcribe_from_link(link, target_lan, openai_apikey, translation_model):
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
		json_file = base + ".vtt"
        
		# check if file exists
		if not os.path.exists(json_file):
            # if vtt file does not exist, we create it
			model = whisper.load_model("tiny")
			result = model.transcribe(file_mp4)
            
            # Save original caption_data
			caption_data = whisper_segments_to_vtt_data(result['segments'])
			file_vtt = base + '.vtt'
			export_file = pathlib.Path(file_vtt)
			export_file.write_text(caption_data)

			# json_object = json.dumps(result, indent=4)
			# with open(base + ".json", "w") as outfile:
			# 	outfile.write(json_object)

			with open(os.path.join(webapp_path, "video_list.txt"), "a") as file_object:
				file_object.write(f"{yt.title}: {link}\n")

			output = translate_text(output=result, target_lan=target_lan, openai_apikey=openai_apikey, translation_model=translation_model)

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
        id=extract.video_id(url)

        # start transcribe
        base = transcribe_from_link(link=url, target_lan=target_lan, openai_apikey=openai_apikey, translation_model=translation_model)
        print(f"Generating trascript DONE at {base}")
        return redirect(url_for('success', name=id, target_lan=target_lan))


if __name__ == '__main__':
    app.run(debug=True)