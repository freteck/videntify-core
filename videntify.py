import asyncio
from shazamio import Shazam
import sounddevice as sd
from pydub import AudioSegment
import io
from gui import run_gui

async def identify_song(audio: bytes):
  shazam = Shazam()
  out = await shazam.recognize(audio)  # rust version, use this!
  return out


def record_audio(duration=5, sample_rate=44100, output_path="temp_recording.mp3"):
  audio_data = sd.rec(int(sample_rate*duration), samplerate=sample_rate, channels=1, dtype='int16')
  sd.wait()
  audio_segment = AudioSegment(
    data=audio_data.tobytes(),
    sample_width=audio_data.dtype.itemsize,
    frame_rate=sample_rate,
    channels=1
  )
  buf = io.BytesIO()
  audio_segment.export(buf, format="mp3")
  mp3 = buf.getvalue()
  buf.close()
  return mp3

async def main():
  while(1):
    match = None
    rec_duration = 5
    audio = record_audio(rec_duration)
    print("Audio Captured (5s)")
    identification_data = await identify_song(audio)
    if len(identification_data["matches"]) > 0:
      match = identification_data["track"]
      print(match["title"] + " - " + match["subtitle"])
    else: 
      print("Song Not Detected")
    await asyncio.sleep(1)

# Main thread
if __name__ == "__main__":
  run_gui()