import psycopg2
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from SakthiLibrary import MenuItems

from random import randint
import os, os.path

root = Tk()

DIR = "E://Python_Classes//GUI_FormsTraining//images"
img = randint(1, len(os.listdir(DIR)))
imgpic = Image.open(f"E://Python_Classes//GUI_FormsTraining//images/{img}.jpg")


resized = imgpic.resize((800, 800), Image.ANTIALIAS)
image = ImageTk.PhotoImage(resized)
thunai_txt=Label(root, text="மாலைக்காரியம்மன் துணை", font=("Arial Unicode MS", 10, 'bold'), bg="#4E806A", fg="yellow")
thunai_txt.pack()
welcome_txt=Label(root, text="சக்தி நூலகம் அன்புடன் வரவேற்கிறது!", font=("Arial Unicode MS", 30, 'bold'), bg="#4E806A", fg="white")
welcome_txt.pack(padx=5, pady=5)

panel = Label(root, image=image, bd=0, height=800, width=800)
panel.place(x=525, y=150)
#panel.pack(fill="y", expand="no")

root.config(bg="#4E806A")

menu_bar = MenuItems.MenuBar
MenuItems.MenuBar(root)
root.mainloop()
