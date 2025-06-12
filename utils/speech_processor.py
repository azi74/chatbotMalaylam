import speech_recognition as sr
from pydub import AudioSegment
import os
from config import Config

def process_audio(audio_file):
    """Process Malayalam audio file and convert to text"""
    try:
        # Save the uploaded file temporarily
        filename = os.path.join(Config.AUDIO_UPLOAD_FOLDER, audio_file.filename)
        audio_file.save(filename)
        
        # Convert to WAV if needed
        if not filename.endswith('.wav'):
            audio = AudioSegment.from_file(filename)
            wav_filename = os.path.splitext(filename)[0] + '.wav'
            audio.export(wav_filename, format='wav')
            os.remove(filename)
            filename = wav_filename
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Recognize Malayalam speech
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='ml-IN')
        
        # Clean up
        os.remove(filename)
        
        return text
    
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None