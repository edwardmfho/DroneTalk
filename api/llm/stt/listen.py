import logging

from openai import OpenAI
from dotenv import load_dotenv

from api.model.audios import VerbalCommands

logging.basicConfig(level=logging.INFO)

def transcribe_audio(speech: VerbalCommands):
    """
    Transcribes the audio file specified in the `speech` object using the Whisper-1 model.

    Args:
        speech (VerbalCommands): The VerbalCommands object containing the path to the audio file.

    Returns:
        VerbalCommands: The updated VerbalCommands object with the transcribed content.
    """
    try:
        audio_file = open(speech.path, "rb")
    except FileNotFoundError:
        logging.error("Audio file not found.")
    
    # Transcribe command
    logging.info("Transcribing verbal commands...")
    speech.content = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format="text"
    )
    logging.info("Transcription complete.")
    return speech

if __name__ == '__main__':
    load_dotenv()
    client = OpenAI()
    test_audio = VerbalCommands(path='assets/audio/audio_test.mp3')

    audio = transcribe_audio(test_audio)
    print(audio.content)