import streamlit as st
import whisper
import json 
from pytube import YouTube
import os

st.set_page_config(layout="wide", page_title="YouTube Transcription")


# Initialization
if 'status' not in st.session_state:
    st.session_state['status'] = 'pending'
if 'json_file' not in st.session_state:
    st.session_state['json_file'] = ''
if 'transcript' not in st.session_state:
    st.session_state['transcript'] = ''

status = "pending"
json_file = ""
# transcription = ""

@st.cache
def transcribe_from_link(link):
	if link != "":
		print("Transcribing...")	
		yt = YouTube(link)
		video = yt.streams.filter(only_audio=True).first()
		
		# # check for destination to save file
		destination = '.'
		
		# download the file
		out_file = video.download(output_path=destination)
		print(yt.title + " has been downloaded successfully")

		# save the file
		base, ext = os.path.splitext(out_file)
		new_file = base + '.mp3'
		os.rename(out_file, new_file)
		
		# result of success
		global json_file
		json_file = base + ".json"
		global transcription

		# check if file exists
		if not os.path.exists(json_file):
			model = whisper.load_model("small")
			result = model.transcribe(new_file)
			# transcription = result['text']
			st.session_state['transcript'] = result['text']
			json_object = json.dumps(result, indent=4)
			with open(json_file, "w") as outfile:
				outfile.write(json_object)
		else:
			f = open(json_file)
			data = json.load(f)
			# transcription = data['text']
			st.session_state['transcript'] = data['text']
			f.close()

		# delete the mp3 file
		if os.path.exists(new_file):
			os.remove(new_file)
			print("The file has been deleted successfully")
		else:
			print("The file does not exist!")

		# Change status to completed	
		global status 
		status = "completed"
		return "completed"
	
st.title('Easily transcribe YouTube videos')

col1, col2 = st.columns(2)

with col1:
	link = st.text_input('Enter YouTube link and wait to get your transcript, don\'t click the submit button', '')
	if link != "":
		st.video(link)

with col2:
	# st.text("Enter and wait to get your transcript, don't click the submit button")	
	st.button("Submit", on_click=transcribe_from_link(link))
	st.write(st.session_state['transcript'])




 