#!/usr/bin/python

from Tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os

PIC_PATH = "Courant-library-floorplan.jpg"

FONT_PATH = os.environ.get("FONT_PATH", "/Library/Fonts/Times New Roman.ttf")

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def drawImage(self):
        draw = ImageDraw.Draw(self.courantLibMap)
        font = ImageFont.truetype("Times New Roman.ttf", 30)
        cor1 = (921, 436)
        cor2 = (751, 433)
        cor3 = (621, 438)
        cor4 = (519, 433)
        cor5 = (335, 372)
        cor6 = (159, 376)
        cor7 = (103, 424)
        cor8 = (106, 265)
        cor9 = (109, 103)
        cor10 = (223, 181)
        cor11 = (248, 59)
        cor12 = (336, 184)
        cor13 = (338, 271)
        cor14 = (490, 181)
        cor15 = (708, 175)
        cor16 = (856, 173)
        cor17 = (756, 65)
        cor18 = (938, 62)
        cor19 = (917, 245)
        cor20 = (862, 364)
        draw.text(cor1, "1", fill="red", font=font)
        draw.text(cor2, "2", fill="red", font=font)
        draw.text(cor3, "3", fill="red", font=font)
        draw.text(cor4, "4", fill="red", font=font)
        draw.text(cor5, "5", fill="red", font=font)
        draw.text(cor6, "6", fill="red", font=font)
        draw.text(cor7, "7", fill="red", font=font)
        draw.text(cor8, "8", fill="red", font=font)
        draw.text(cor9, "9", fill="red", font=font)
        draw.text(cor10, "10", fill="red", font=font)
        draw.text(cor11, "11", fill="red", font=font)
        draw.text(cor12, "12", fill="red", font=font)
        draw.text(cor13, "13", fill="red", font=font)
        draw.text(cor14, "14", fill="red", font=font)
        draw.text(cor15, "15", fill="red", font=font)
        draw.text(cor16, "16", fill="red", font=font)
        draw.text(cor17, "17", fill="red", font=font)
        draw.text(cor18, "18", fill="red", font=font)
        draw.text(cor19, "19", fill="red", font=font)
        draw.text(cor20, "20", fill="red", font=font)
        del draw

    def createWidgets(self):
        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack({"side": "top"})

        # self.img = ImageTk.PhotoImage(self.courantLibMap)
        # self.panel = Label(self, image=self.img)
        # self.panel.pack(side="bottom", fill="both", expand="yes")

        self.frame = Frame(self, bd=2, relief=SUNKEN)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self.frame, bd=0, height=547, width=1029)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)

        self.frame.pack(fill=BOTH, expand=1)

        self.img = ImageTk.PhotoImage(self.courantLibMap)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        def printcoords(event):
            # outputting x and y coords to console
            print (event.x, event.y)

            draw = ImageDraw.Draw(self.courantLibMap)
            new_cor = (event.x, event.y)
            font = ImageFont.truetype("Times New Roman.ttf", 30)
            r = 2
            draw.ellipse((event.x - r, event.y - r, event.x + r, event.y + r), fill=(0, 255, 0, 0))
            draw.text(new_cor, "target", fill=(0, 255, 0, 0), font=font)
            del draw

            # update image
            self.img = ImageTk.PhotoImage(self.courantLibMap)
            self.canvas.create_image(0, 0, image=self.img, anchor="nw")
            self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        # mouseclick event
        self.canvas.bind("<Button 1>", printcoords)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.courantLibMap = Image.open(PIC_PATH)
        self.drawImage()
        self.createWidgets()


def gui():
    root = Tk()
    app = Application(master=root)
    app.mainloop()


def getCoordinate():
    root = Tk()
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    canvas = Canvas(frame, bd=0, height=547, width=1029)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)

    frame.pack(fill=BOTH,expand=1)

    img = ImageTk.PhotoImage(Image.open(PIC_PATH))
    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    def printcoords(event):
        #outputting x and y coords to console
        print (event.x, event.y)
    #mouseclick event
    canvas.bind("<Button 1>", printcoords)

    root.mainloop()

if __name__ == "__main__":
    gui()
    # getCoordinate()
