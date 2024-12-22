import asyncio
from shazamio import Shazam
import sounddevice as sd
from pydub import AudioSegment
import tkinter as tk
from PIL import Image, ImageFilter, ImageTk
import io, requests

SILENCE_ALBUM_ART_URL = "https://i.ibb.co/72J3zjF/silent.png"

shazam = Shazam()

root = tk.Tk()
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


update_cover_art(SILENCE_ALBUM_ART_URL)

canvas.pack()

text_x_offset = 40 + album_art_size[0] + 40
text_y_offset = 300
shadow_offset = 4
text_y_margin = 0

y_offset = ((root.winfo_height() - album_art_size[1])/2) + 40

image_label.place(x=40, y = y_offset)

# Globals
song_label_shadow = None
song_label = None
album_label_shadow = None
album_label = None
artist_label_shadow = None
artist_label = None

def draw_text():
  global song
  global album_title
  global artist
  global song_label_shadow 
  global song_label
  global album_label_shadow
  global album_label
  global artist_label_shadow
  global artist_label

  text_items = [song_label_shadow, album_label_shadow, song_label, album_label, artist_label_shadow, artist_label]
  for item in text_items:
    canvas.delete(item)
  
  adj_song_height = text_y_offset + (40 * (len(song) // 16))

  canvas.create_text(40 + shadow_offset, 100 + shadow_offset, text="Now Playing:", font="calibri 70 bold", fill="black", anchor="w", width=root.winfo_width() - text_x_offset - 40)
  canvas.create_text(40, 100, text="Now Playing:", font="calibri 70 bold", fill="white", anchor="w", width=root.winfo_width() - text_x_offset - 40)

  song_label_shadow = canvas.create_text(text_x_offset + shadow_offset, adj_song_height + shadow_offset, text=song, font="calibri 100 bold", fill="black", anchor="w", width=root.winfo_width() - text_x_offset - 40)
  song_label = canvas.create_text(text_x_offset, adj_song_height, text=song, font="calibri 100 bold", fill="white", anchor="w", width=root.winfo_width() - text_x_offset - 40)
  song_title_height = canvas.bbox(song_label)[3] - canvas.bbox(song_label)[1]

  album_label_shadow = canvas.create_text(text_x_offset + shadow_offset, text_y_offset + shadow_offset + song_title_height + text_y_margin, text=album_title, font="calibri 40 bold", fill="black", anchor="w", width=root.winfo_width() - text_x_offset - 40)
  album_label = canvas.create_text(text_x_offset, text_y_offset + song_title_height + text_y_margin, text=album_title, font="calibri 40 bold", fill="white", anchor="w", width=root.winfo_width() - text_x_offset - 40)
  album_title_height = canvas.bbox(album_label)[3] - canvas.bbox(album_label)[1]

  artist_label_shadow = canvas.create_text(text_x_offset + shadow_offset, text_y_offset + shadow_offset + song_title_height + album_title_height + 2*text_y_margin, text=artist, font="calibri 40 italic", fill="black", anchor="w", width=root.winfo_width() - text_x_offset - 40)
  artist_label = canvas.create_text(text_x_offset, text_y_offset + song_title_height + album_title_height + 2*text_y_margin, text=artist, font="calibri 40 italic", fill="white", anchor="w", width=root.winfo_width() - text_x_offset - 40)

def record_audio(duration=5, sample_rate=44100):
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
      print(match["title"] + " - " + match["subtitle"])
      song = match["title"]
      try:
        album_title = match["sections"][0]["metadata"][0]["text"]
        artist = match["subtitle"]
        canvas.itemconfig(song_label, text=song)
        canvas.itemconfig(song_label_shadow, text=song)

        canvas.itemconfig(album_label, text=album_title)
        canvas.itemconfig(album_label_shadow, text=album_title)

        canvas.itemconfig(artist_label, text=artist)
        canvas.itemconfig(artist_label_shadow, text=artist)
        draw_text()
        update_cover_art(match["images"]["coverart"])
      except:
        pass
    else: 
      print("Song Not Detected")
      song = "Silence 😴"
      album_title = "Play a record to begin recognition"
      artist = ""
      draw_text()
      update_cover_art(SILENCE_ALBUM_ART_URL)
  else:
    init_complete += 1
  root.after(100, identify_song)


# Main thread
if __name__ == "__main__":
  draw_text()
  identify_song()
  root.mainloop()
