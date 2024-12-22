import asyncio
from shazamio import Shazam
import sounddevice as sd
from pydub import AudioSegment
import tkinter as tk
from PIL import Image, ImageFilter, ImageTk
import io, requests

root = tk.Tk()
shazam = Shazam()
init_complete = 0


song = "Silence 😴"
album_title = "Play a record to begin recognition"
artist = ""
root.attributes("-fullscreen", True)
canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height(), highlightthickness=0)

root.title("Videntify")

tk_bg = None
album_cover_art_image = canvas.create_image(0, -((root.winfo_width() - root.winfo_height()) / 2), image=tk_bg, anchor="nw")  # Place the image on the canvas
album_art = tk.PhotoImage(file="image.png")
album_art_size = (album_art.width(), album_art.height())
image_label = tk.Label(root, image=album_art)

def update_cover_art(cover_art_url):
  global tk_bg
  response = requests.get(cover_art_url)
  response_image = Image.open(io.BytesIO(response.content))
  cover_art = ImageTk.PhotoImage(response_image.resize((512, 512)))
  image_label.config(image=cover_art)
  image_label.image = cover_art

  cover = response_image.convert("RGB").resize((root.winfo_width(), root.winfo_width()))
  bg = cover.filter(ImageFilter.GaussianBlur(20))
  bg_bytes = io.BytesIO()
  bg.save(bg_bytes, format="JPEG")
  bg_bytes.seek(0)
  tk_bg = ImageTk.PhotoImage(Image.open(bg_bytes))
  canvas.itemconfig(album_cover_art_image, image=tk_bg)


update_cover_art("https://i.ibb.co/72J3zjF/silent.png")

canvas.pack()


y_offset = (root.winfo_height() - album_art_size[1])/2

image_label.place(x=40, y = y_offset)

text_x_offset = 40 + album_art_size[0] + 40
shadow_offset = 4

# draw text
song_label_shadow = canvas.create_text(text_x_offset + shadow_offset, 261 + shadow_offset, text=song, font="calibri 100 bold", fill="black", anchor="w", width=root.winfo_width() - text_x_offset - 40)
song_label = canvas.create_text(text_x_offset, 261, text=song, font="calibri 100 bold", fill="white", anchor="w", width=root.winfo_width() - text_x_offset - 40)

album_label_shadow = canvas.create_text(text_x_offset + shadow_offset, 400 + shadow_offset, text=album_title, font="calibri 40 bold", fill="black", anchor="w", width=root.winfo_width() - text_x_offset - 40)
album_label = canvas.create_text(text_x_offset, 400, text=album_title, font="calibri 40 bold", fill="white", anchor="w", width=root.winfo_width() - text_x_offset - 40)

artist_label_shadow = canvas.create_text(text_x_offset + shadow_offset, 460 + shadow_offset, text=artist, font="calibri 40 italic", fill="black", anchor="w", width=root.winfo_width() - text_x_offset - 40)
artist_label = canvas.create_text(text_x_offset, 460, text=artist, font="calibri 40 italic", fill="white", anchor="w", width=root.winfo_width() - text_x_offset - 40)

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

def identify_song():
  global song
  global album_title
  global artist
  global init_complete

  if init_complete > 2:
    print("Attempting Song Identification")
    rec_duration = 5
    audio = record_audio(rec_duration)
    print("Audio Captured (5s)")
    identification_data = asyncio.run(shazam.recognize(audio))
    if len(identification_data["matches"]) > 0:
      match = identification_data["track"]
      print(match)
      print(match["title"] + " - " + match["subtitle"])
      song = match["title"]
      canvas.itemconfig(song_label, text=match["title"])
      canvas.itemconfig(song_label_shadow, text=match["title"])

      canvas.itemconfig(album_label, text=match["sections"][0]["metadata"][0]["text"])
      canvas.itemconfig(album_label_shadow, text=match["sections"][0]["metadata"][0]["text"])

      canvas.itemconfig(artist_label, text=match["subtitle"])
      canvas.itemconfig(artist_label_shadow, text=match["subtitle"])
      update_cover_art(match["images"]["coverart"])
    else: 
      print("Song Not Detected")
  else:
    init_complete += 1
  root.after(100, identify_song)


# Main thread
if __name__ == "__main__":
    # init_gui()
    identify_song()
    root.mainloop()
