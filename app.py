import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
import os

def convert_audio_to_wav(input_path, output_path):
    """Convert MP3 or M4A to WAV."""
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

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

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
text_input = st.text_area("Or enter text to translate")

if st.button("Translate"):
    text = ""
    if uploaded_file is not None:
        input_ext = uploaded_file.name.split(".")[-1]
        temp_path = f"temp_audio.{input_ext}"
        wav_path = "converted_audio.wav"

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        if input_ext in ["mp3", "m4a"]:
            convert_audio_to_wav(temp_path, wav_path)
        else:
            wav_path = temp_path  # Already in WAV format

        text = speech_to_text(wav_path)
    
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

    # Clean up temporary files
    if os.path.exists(temp_path):
        os.remove(temp_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)
