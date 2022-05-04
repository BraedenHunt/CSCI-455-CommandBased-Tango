from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        
    def healthBar(self, health):
        canvas = Canvas(self, width = 300, height = 70, highlightthickness=0)
        canvas.configure(bg='black')
        newHealth = health + 50
        canvas.create_text(70, 15, text="HEALTH", fill="white", font=('Helvetica 15 bold'))
        # Health bounds 0 & 200
        canvas.create_rectangle(50, 55, 250, 30, fill = 'white')
        canvas.create_rectangle(50, 55, newHealth, 30, fill = 'green', outline='')
        canvas.pack(side = LEFT, padx = 0, pady = 0, anchor = NW)
        
    def drinkPotion(self, fileName):
        gif = Image.open(fileName)
        frames = gif.n_frames
        im = [PhotoImage(file=fileName,format=f"gif -index {i}") for i in range(frames)]
        count = 0
        anim = None

        def animation(count):
            global anim
            im2 = im[count]

            gif_label.configure(image=im2)
            count += 1
            if count == frames:
                count = 0
            anim = root.after(50,lambda :animation(count))
        
        gif_label = Label(self,image="")
        gif_label.place(x=600, y=0)
        gif_label.configure(bg='black', fg='white')

        animation(count)
        resized_gif = gif.resize((800, 480), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resized_gif)
    
    def loadBlade(self, fileName):
        gif = Image.open(fileName)
        frames = gif.n_frames
        im = [PhotoImage(file=fileName,format=f"gif -index {i}") for i in range(frames)]
        count = 0
        anim = None

        def animation(count):
            global anim
            im2 = im[count]

            gif_label.configure(image=im2)
            count += 1
            if count == frames:
                count = 0
            anim = root.after(50,lambda :animation(count))
        
        gif_label = Label(self,image="")
        gif_label.place(x=500, y=0)
        gif_label.configure(bg='black', fg='white')

        animation(count)
        resized_gif = gif.resize((800, 480), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resized_gif)

    def loadImage(self, fileName):
        img = Image.open(fileName)
        resized_img = img.resize((800, 480), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resized_img)
        img = Label(self, image=render, borderwidth = 0)
        img.image = render
        img.place(x=0, y=0)
        
    def loadEnemy(self, fileName, health):
        gif = Image.open(fileName)
        frames = gif.n_frames
        im = [PhotoImage(file=fileName,format=f"gif -index {i}") for i in range(frames)]
        count = 0
        anim = None

        def animation(count):
            global anim
            im2 = im[count]

            gif_label.configure(image=im2)
            count += 1
            if count == frames:
                count = 0
            anim = root.after(50,lambda :animation(count))
        
        label = Label(self, text=str(health))
        label.pack(side=RIGHT, anchor=SE)
        label.configure(bg='black', fg='white')
        gif_label = Label(self,image="", width=115, height=115)
        gif_label.pack(side=RIGHT, anchor=SE)
        gif_label.configure(bg='black', fg='white')

        animation(count)
        resized_gif = gif.resize((100, 100), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resized_gif)
        
    def loadKey(self, fileName):
        img = Image.open(fileName)
        resized_img = img.resize((75, 75), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(resized_img)
        img = Label(self, image=render, borderwidth = 0)
        img.configure(bg='black')
        img.image = render
        img.place(x=700, y=0)
    
root = Tk()
app = Window(root)
root.wm_title("Background")
root.geometry("800x480")
app.loadImage("guiPics/dungeon_three.jpeg")
app.drinkPotion("guiPics/potion5.gif")
app.loadBlade("guiPics/blade3.gif")
app.loadEnemy("guiPics/orc.gif", 1)
app.loadEnemy("guiPics/slime.gif", 2)
app.loadEnemy("guiPics/demon.gif", 3)
app.loadKey("guiPics/key.jpeg")
app.healthBar(100)
root.mainloop()
