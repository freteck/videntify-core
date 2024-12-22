import tkinter as tk
from PIL import Image, ImageFilter, ImageTk
import io

def run_gui():
  song = "Dark Fantasy"
  album_title = "My Beautiful Dark Twisted Fantasy"
  artist = "Kanye West"

  root = tk.Tk()
  root.title("Videntify")
  root.attributes("-fullscreen", True)

  bg = Image.open("image.png").convert("RGB").resize((root.winfo_width(), root.winfo_width()))
  bg = bg.filter(ImageFilter.GaussianBlur(20))
  bg_bytes = io.BytesIO()
  bg.save(bg_bytes, format="JPEG")
  bg_bytes.seek(0)
  tk_bg = ImageTk.PhotoImage(Image.open(bg_bytes))

  canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height(), highlightthickness=0)
  canvas.create_image(0, -((root.winfo_width() - root.winfo_height()) / 2), image=tk_bg, anchor="nw")  # Place the image on the canvas
  canvas.pack()

  album_art = tk.PhotoImage(file="image.png")
  album_art_size = (album_art.width(), album_art.height())
  image_label = tk.Label(root, image=album_art)
  y_offset = (root.winfo_height() - album_art_size[1])/2

  image_label.place(x=40, y = y_offset)
  
  text_x_offset = 40 + album_art_size[0] + 40
  shadow_offset = 4

  # draw text
  canvas.create_text(text_x_offset + shadow_offset, 261 + shadow_offset, text=song, font="calibri 100 bold", fill="black", anchor="w")
  canvas.create_text(text_x_offset, 261, text=song, font="calibri 100 bold", fill="white", anchor="w")

  canvas.create_text(text_x_offset + shadow_offset, 361 + shadow_offset, text=album_title, font="calibri 40 bold", fill="black", anchor="w")
  canvas.create_text(text_x_offset, 361, text=album_title, font="calibri 40 bold", fill="white", anchor="w")

  canvas.create_text(text_x_offset + shadow_offset, 430 + shadow_offset, text=artist, font="calibri 40 italic", fill="black", anchor="w")
  canvas.create_text(text_x_offset, 430, text=artist, font="calibri 40 italic", fill="white", anchor="w")

  # track_name_label = tk.Label(root, textvariable=track_name, font=("Arial", 50), bg=None)
  # album_label = tk.Label(root, textvariable=album_name, font=("Arial", 30), bg=None)
  # artist_label = tk.Label(root, textvariable=artist_name, font=("Arial", 30), bg=None)


  # track_name_label.place(x=album_art_size[0] + 100, y = y_offset)
  # album_label.place(x=album_art_size[0] + 100, y = y_offset + 90)
  # artist_label.place(x=album_art_size[0] + 100, y = y_offset + 180)

  # bg_label.lower()

  root.mainloop()

run_gui()