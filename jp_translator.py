from deep_translator import GoogleTranslator
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
from PIL import Image
import speech_recognition as sr
import streamlit as st


from IPython.display import Audio


def speech_to_text(path, engine):
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
    # google
    if engine == "google":
        try:
            with st.empty():
                st.write("google recognizing speech...")
                text = recognizer.recognize_google(audio, language="ja")
                if text:
                    st.empty()
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition")
    # wit ai
    elif engine == "wit":
        try:
            with st.empty():
                st.write("wit ai recognizing speech...")
                text = recognizer.recognize_wit(audio, key="EnterYourKey")
                if text:
                    st.empty()
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition")
    else:
        raise ValueError("Invalid engine: " + engine)

def google_translate(text, source, target):
    translator = GoogleTranslator(source=source, target=target)
    with st.empty():
        st.write("translating...")
        result = translator.translate(text)
        if result:
            st.empty()
    return result

def text_to_speech(text,lang):
    speech = gTTS(text = text, lang = lang, slow = False)
    speech.save('jp.mp3')
    audio_file = open('jp.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg',start_time=0)
"""--------------------------------------------------------------------------------------------------------------------------------"""

#image for top of the screen
image = Image.open('./jp_translator.jpeg')
st.image(image)

#Text Display
st.title(f"Japanese Text/Speech Translator")


def add_fields():
    col1, col2 = st.columns(2)
  # Part I:Translates user input and creates text to speech audio
    with col1:
        st.header("Text to Speech")
        input_text = st.text_input('Enter Japanese Text:', value='こんにちは')
        if st.button('Translate'):
            result = google_translate(text=input_text,source='auto', target='zh-CN')
            st.success(result)
            text_to_speech(text = input_text,lang="ja")
  #Part II: Record Japanese Audio
    with col2:
    #audio recoginzer
        st.header("Speech to Text")
        audio_bytes = audio_recorder(text="Record Japanese Audio")
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
    # Save the audio as a file
            with open("input_audio.wav", "wb") as f:
                f.write(audio_bytes)
                f.close()
    # Load the audio file
            src_text = speech_to_text("input_audio.wav", engine="wit")
            st.write("Src: " + src_text)
            trans_text = google_translate(text=src_text, source='auto', target='zh-CN')
            st.write("Trans: " + trans_text)
            text_to_speech(text=src_text,lang="ja")

if __name__ == "__main__":
  add_fields()
