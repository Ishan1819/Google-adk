import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import whisper
import google.generativeai as genai
import os
from pathlib import Path
import logging
import numpy as np

# ----------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------
GENIE_API_KEY = "AIzaSyDUDtg07eUs3RwH7W8cLagv0s-UjmPd660"
genai.configure(api_key=GENIE_API_KEY)

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

logger.info("Loading Whisper model...")
WHISPER_MODEL = whisper.load_model("small")
logger.info("Whisper model loaded\n")

# ----------------------------------------------------------
# AUDIO DEVICE DETECTION
# ----------------------------------------------------------
def get_default_samplerate():
    """
    Get the default sample rate for the default input device
    """
    try:
        device_info = sd.query_devices(kind='input')
        samplerate = int(device_info['default_samplerate'])
        logger.info(f"Using device: {device_info['name']}")
        logger.info(f"Sample rate: {samplerate} Hz")
        return samplerate
    except Exception as e:
        logger.warning(f"Could not detect sample rate, using 16000 Hz: {e}")
        return 16000

# ----------------------------------------------------------
# AUDIO RECORDING
# ----------------------------------------------------------
def record_voice(duration=6):
    """
    Record voice from default microphone with auto-detected sample rate
    """
    temp_wav = None
    try:
        # Auto-detect sample rate
        samplerate = get_default_samplerate()
        
        logger.info(f"\nRecording for {duration} seconds... SPEAK NOW!")
        logger.info("=" * 50)
        
        audio = sd.rec(
            int(duration * samplerate), 
            samplerate=samplerate, 
            channels=1, 
            dtype='int16'
        )
        sd.wait()
        
        # Check audio level
        audio_level = np.max(np.abs(audio))
        logger.info(f" Audio level: {audio_level}")
        
        if audio_level < 100:
            logger.warning(" Audio level is very low! Please speak louder.")
        
        # Save temp WAV file
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        temp_wav = temp_dir / "input_audio.wav"
        write(str(temp_wav), samplerate, audio)
        logger.info(f" Audio saved to {temp_wav}\n")
        return str(temp_wav)
        
    except Exception as e:
        logger.error(f" Error recording audio: {e}")
        logger.error("Troubleshooting tips:")
        logger.error("  1. Check if microphone is connected")
        logger.error("  2. Check Windows sound settings")
        logger.error("  3. Try running as administrator")
        return None

# ----------------------------------------------------------
# WHISPER TRANSCRIPTION & LANGUAGE DETECTION
# ----------------------------------------------------------
def whisper_transcribe(audio_path):
    """
    Transcribe audio and detect language using Whisper
    """
    if not audio_path or not os.path.exists(audio_path):
        logger.error("Invalid audio file path")
        return None, None

    logger.info("Transcribing with Whisper...")
    try:
        result = WHISPER_MODEL.transcribe(audio_path, fp16=False)
        transcription = result["text"].strip()
        detected_lang = result.get("language", "unknown")
        
        # Get language name
        lang_name = whisper.tokenizer.LANGUAGES.get(detected_lang, detected_lang)
        
        logger.info(f"Transcription complete!")
        logger.info(f"Detected Language: {lang_name.title()} ({detected_lang})")
        logger.info(f"Transcribed Text:\n   '{transcription}'\n")
        
        return transcription, lang_name
        
    except Exception as e:
        logger.error(f"Whisper transcription error: {e}")
        return None, None

# ----------------------------------------------------------
# GEMINI TRANSLATION
# ----------------------------------------------------------
def gemini_translate(original_text, source_lang):
    """
    Translate into English and Hindi using Gemini
    """
    if not original_text:
        return "No text to translate"

    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    prompt = f"""You are a professional translator. 

Source Language: {source_lang}
Source Text: {original_text}

Provide translations in this exact format:

**English:** [translation]
**Hindi:** [translation]

Be accurate and natural. Maintain the tone and meaning."""

    try:
        logger.info("Translating with Gemini...")
        response = model.generate_content(prompt)
        logger.info("Translation complete!\n")
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini translation error: {e}")
        return f"Translation error: {e}"

# ----------------------------------------------------------
# MAIN FLOW
# ----------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" WHISPER + GEMINI VOICE TRANSLATOR")
    print("=" * 60 + "\n")

    # Step 1: Record audio
    audio_file = record_voice(duration=6)
    if not audio_file:
        logger.error("Failed to record audio. Exiting.")
        exit(1)

    # Step 2: Transcribe with Whisper
    text, lang = whisper_transcribe(audio_file)
    if not text:
        logger.error("Failed to transcribe audio. Exiting.")
        exit(1)

    # Step 3: Translate with Gemini
    translations = gemini_translate(text, lang)

    # Step 4: Display results
    print("=" * 60)
    print("TRANSLATIONS")
    print("=" * 60)
    print(translations)
    print("=" * 60 + "\n")

    # Clean up temp audio
    if audio_file and os.path.exists(audio_file):
        try:
            os.remove(audio_file)
            logger.info(" Cleaned up temporary audio file")
        except Exception as e:
            logger.error(f" Could not delete temp file: {e}")