
import pathlib
import math
from pathlib import Path
import config as cfg
import assemblyai as aai

from openai import OpenAI

client = OpenAI(api_key=cfg.OPENAI_API_KEY)
from pydub import AudioSegment
from moviepy.editor import AudioFileClip



def _transcribe_with_whisper(audio_file_path: str):
    with open(audio_file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(model="whisper-1", file=f)
    return transcription.text

def _transcribe_with_assemblyai(audio_file_path: str, identify_speakers: bool, language_code: str) -> str:
    transcriber = aai.Transcriber()
    if identify_speakers:
        config = aai.TranscriptionConfig(speaker_labels=True, language_code=language_code)
        transcript = transcriber.transcribe(audio_file_path,config=config)
        assert transcript is not None and transcript.utterances is not None, "Something went wrong with transcription"
        result = ""
        for utterance in transcript.utterances:
            result += f"Speaker {utterance.speaker}: {utterance.text}\n"
        return result
    else:
        # Replace with your API key
        config = aai.TranscriptionConfig(language_code=language_code)
        transcript = transcriber.transcribe(audio_file_path, config=config)
        assert transcript.text is not None, "Something went wrong with transcription"
        return transcript.text


def convert_to_mp3(input_file, output_file):
    clip = AudioFileClip(input_file)
    clip.write_audiofile(output_file)
    clip.close()


def split_mp3(input_file: str, output_prefix: str, folder_path: pathlib.Path, duration: int = 300000):
    folder_path = Path(folder_path)
    audio = AudioSegment.from_mp3(input_file)
    total_duration = len(audio)
    num_parts = math.ceil(total_duration / duration)

    for i in range(num_parts):
        start_time = i * duration
        end_time = min((i + 1) * duration, total_duration)
        part = audio[start_time:end_time]
        path_template = str(folder_path / f"{output_prefix}_") + "{}.mp3"
        output_file = path_template.format(i + 1)
        part.export(output_file, format="mp3")
        print(f"Exported {output_file}")

    return num_parts, path_template


def transcribe_mp3_file(path: str, identify_speakers: bool = False, language_code: str = "en") -> str:
    return _transcribe_with_assemblyai(path, identify_speakers, language_code)

def transcribe_mp3_group(file_template: str, num_parts: int, identify_speakers: bool = False) -> str:
    transcripts = []
    for i in range(num_parts):
        path = str(file_template.format(i + 1))
        transcript = _transcribe_with_assemblyai(path, identify_speakers)
        transcripts.append(transcript)
    full_text = "\n\n".join(transcripts)
    return full_text

