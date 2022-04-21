from tkinter import *
from PIL import Image

class Animation:
    def __init__(self):
        self.root = Tk()
        self.file = "robot_eyes.gif"
        self.info = Image.open(self.file)

        self.frames = self.info.n_frames
        self.im = [PhotoImage(file=self.file,format=f"gif -index {i}") for i in range(self.frames)]

        self.count = 0
        self.anim = None
        self.gif_label = Label(self.root, image="")
        self.gif_label.pack()

    def start(self):
        self.animation()
        self.root.mainloop()

    def animation(self):
        im2 = self.im[self.count]

        self.gif_label.configure(image=im2)
        self.count += 1
        if self.count == self.frames:
            self.count = 0
        self.anim = self.root.after(50,lambda :self.animation())

if __name__ == "__main__":
    a = Animation()
    a.start()
    print("test")


