import json
import wave
import pyttsx3
from transformers import pipeline
from vosk import Model, KaldiRecognizer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
import os
import logging

# Setup logging
logger = logging.getLogger(__name__)

class VoiceBot(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            # Initialize STT (Vosk)
            self.stt_model = Model('D:\\vosk-model-en-us-0.22-lgraph')
            
            # Initialize TTS (pyttsx3)
            self.tts_engine = pyttsx3.init()
            
            # Initialize LLM (Transformers)
            self.llm_model = pipeline('text-generation', model='gpt2')
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if 'audio' not in request.FILES:
            return HttpResponse("No audio file provided.", status=400)

        input_audio = request.FILES['audio']
        input_audio.seek(0)
        
        # Save uploaded audio to a file
        input_audio_path = 'input.wav'
        try:
            with open(input_audio_path, 'wb') as f:
                f.write(input_audio.read())
        except Exception as e:
            logger.error(f"Error saving audio file: {e}")
            return HttpResponse("Error saving audio file.", status=500)

        try:
            # STT: Convert speech to text
            transcript = self.transcribe_speech(input_audio_path)
            
            # LLM: Get response
            llm_response = self.query_llm(transcript)
            
            # TTS: Convert text to speech
            tts_audio = self.synthesize_speech(llm_response)
            
            return HttpResponse(tts_audio, content_type='audio/wav')
        
        finally:
            # Clean up temporary file
            if os.path.exists(input_audio_path):
                os.remove(input_audio_path)

    def transcribe_speech(self, audio_file_path):
        try:
            wf = wave.open(audio_file_path, "rb")
            rec = KaldiRecognizer(self.stt_model, wf.getframerate())
            results = []

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    results.append(json.loads(rec.Result())['text'])
            
            return " ".join(results)
        except Exception as e:
            logger.error(f"Error during speech transcription: {e}")
            return "Error during speech transcription."

    def query_llm(self, user_input):
        try:
            result = self.llm_model(user_input, max_length=50, num_return_sequences=1)
            return result[0]['generated_text']
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            return "Error generating response."

    def synthesize_speech(self, text):
        output_audio_path = 'output.wav'
        try:
            self.tts_engine.save_to_file(text, output_audio_path)
            self.tts_engine.runAndWait()
            
            with open(output_audio_path, 'rb') as f:
                audio_data = f.read()
            
            return audio_data
        except Exception as e:
            logger.error(f"Error during speech synthesis: {e}")
            return b"Error during speech synthesis."
        finally:
            # Clean up temporary file
            if os.path.exists(output_audio_path):
                os.remove(output_audio_path)

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'LLMApp/index.html')
