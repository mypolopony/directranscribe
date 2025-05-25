import whisper
import tempfile
from pathlib import Path

model = whisper.load_model("base")

def transcribe_bytes(audio_bytes: bytes) -> str:
    """
    Transcribe audio from bytes using Whisper model.
    Args:
        audio_bytes (bytes): The audio data in bytes format.
    Returns
        str: The transcribed text from the audio.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp_path = Path(tmp.name)

    result = model.transcribe(str(tmp_path))
    tmp_path.unlink()  # Clean up
    return result["text"]