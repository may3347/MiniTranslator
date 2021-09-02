import streamlit as st 
import os 
import time
import glob

from gtts import gTTS 
from googletrans import Translator

try:
	os.mkdir("temp")
except:
	pass

st.title("Text to Speech")
translator = Translator()

text = st.text_input("Enter text")
in_lang = st.selectbox(
	"Select your input language",
	("Myanmar","English","Chinese","Japanese","Korean"),
)
if in_lang == "Myanmar":
	input_language = "my"
elif in_lang == "English":
	input_language = "en"
elif in_lang == "Chinese":
	input_language = "zh-cn"
elif in_lang == "Japanese":
	input_language = "ja"
elif in_lang == "Korean":
	input_language = "ko"

out_lang = st.selectbox(
	"Select your output language",
	("Myanmar","English","Chinese","Japanese","Korean"),
)
if out_lang == "Myanmar":
	output_language = "my"
elif out_lang == "English":
	output_language = "en"
elif out_lang == "Chinese":
	output_language = "ch"
elif out_lang == "Japanese":
	output_language = "ja"
elif out_lang == "Korean":
	output_language = "ko"

english_accent = st.selectbox(
	"Select your English accent",
	(
		"Default",
		"India",
		"United Kingdom",
		"United States",
		"Canada",
		"Australia",
	),
)

if english_accent == "Default":
	tld = "com"
elif english_accent == "India":
	tld = "co.in"	
elif english_accent == "United Kingdom":
	tld = "co.uk"	
elif english_accent == "United States":
	tld = "com"
elif english_accent == "Canada":
	tld = "ca"
elif english_accent == "Australia":
	tld = "com.au"

def text_to_speech(input_language,output_language,text,tld):
	translation = translator.translate(text, dest=output_language, src=input_language)
	trans_text = translation.text
	tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
	try:
		my_file_name = text[0:20]
	except:
		my_file_name = "audio"
	tts.save(f"temp/{my_file_name}.mp3")
	return my_file_name, trans_text

display_output_text = st.checkbox("Display output text")

if st.button("Convert"):
	result, output_text = text_to_speech(input_language,output_language,text,tld)
	audio_file = open(f"temp/{result}.mp3", "rb")
	audio_bytes = audio_file.read()
	st.markdown(f"## Output text: ")
	st.audio(audio_bytes, format="audio/mp3", start_time=0)

	if display_output_text:
		st.markdown(f"## Output text: ")
		st.write(f"{output_text}")

def remove_file(n):
	mp3_files = glob.glob("temp/*mp3")
	if len(mp3_files) != 0:
		now = time.time()
		n_days = n * 86400 
		for f in mp3_files:
			if os.stat(f).st_mtime < now - n_days:
				os.remove(f)
				print("Deleted ", f)

remove_file(7)