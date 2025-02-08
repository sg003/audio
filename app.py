import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        st.write("Processing audio...")
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except (sr.UnknownValueError, sr.RequestError):
        return None

def translate_text(text, target_lang):
    translator = Translator()
    return translator.translate(text, dest=target_lang).text

def text_to_speech(text, lang, output_filename):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_filename)
    return output_filename

st.title("Speech Translator: English to Tamil & Kannada")

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
text_input = st.text_area("Or enter text to translate")

if st.button("Translate"):
    text = ""
    if uploaded_file is not None:
        filepath = f"temp_audio.{uploaded_file.name.split('.')[-1]}"
        with open(filepath, "wb") as f:
            f.write(uploaded_file.read())
        text = speech_to_text(filepath)
    elif text_input:
        text = text_input
    
    if text:
        tamil_text = translate_text(text, "ta")
        kannada_text = translate_text(text, "kn")
        st.write("### Tamil Translation:")
        st.write(tamil_text)
        st.write("### Kannada Translation:")
        st.write(kannada_text)
        
        tamil_audio = text_to_speech(tamil_text, "ta", "output_tamil.mp3")
        kannada_audio = text_to_speech(kannada_text, "kn", "output_kannada.mp3")
        
        st.audio(tamil_audio, format="audio/mp3")
        st.audio(kannada_audio, format="audio/mp3")