from tkinter import *
from PIL import ImageTk, Image
import os

def photo_root(tk_pil_img):
    root = Tk()

    try:
        old_file = os.path.join("C:/Users/www/PycharmProjects/pythonProject1/my_projects/photos", "000001.png")
        new_file = os.path.join("C:/Users/www/PycharmProjects/pythonProject1/my_projects/photos", "000001.jpg")
        os.rename(old_file, new_file)
    except:
        pass

    try:
        tk_pil_img = ImageTk.PhotoImage(Image.open("photos/000001.jpg"))

        canvas = Canvas(root, width=tk_pil_img.width(), height=tk_pil_img.height())
        canvas.pack()

        photo = ImageTk.PhotoImage(Image.open("photos/000001.jpg"))

        canvas.create_image(0, 0, anchor=NW,image=photo)
    except Exception as e:
        print(e)

    root.mainloop()