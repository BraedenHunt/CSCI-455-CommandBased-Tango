import threading
import time
from tkinter import *
from PIL import Image, ImageTk

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.enemies = []
        self.background_image = None
        self.healthBar_canvas = None

    def harm_enemy(self, index, dmg):
        if not self.enemies[index].deal_damage(dmg):
            self.enemies[index].destroy()
            del self.enemies[index]

    def remove_all_enemies(self):
        for enemy in self.enemies:
            enemy.destroy()
        self.enemies = []

    def set_enemy_health(self, index, hp):
        self.enemies[index].set_health(hp)

    def healthBar(self, health):
        if self.healthBar_canvas is not None:
            self.healthBar_canvas.destroy()
        self.healthBar_canvas = Canvas(self, width = 300, height = 70, highlightthickness=0)
        self.healthBar_canvas.configure(bg='black')
        newHealth = (2*health) + 50
        self.healthBar_canvas.create_text(70, 15, text="HEALTH", fill="white", font=('Helvetica 15 bold'))
        # Health bounds 0 & 200
        self.healthBar_canvas.create_rectangle(50, 55, 250, 30, fill = 'white')
        self.healthBar_canvas.create_rectangle(50, 55, newHealth, 30, fill = 'green', outline='')
        self.healthBar_canvas.pack(side = LEFT, padx = 0, pady = 0, anchor = NW)
        
    def drinkPotion(self, fileName):
        gif = Image.open(fileName)
        frames = gif.n_frames
        im = [PhotoImage(file=fileName,format=f"gif -index {i}") for i in range(frames)]
        count = 0
        anim = None

        def animation(count):
            global anim
            im2 = im[count]
            try:
                gif_label.configure(image=im2)
                count += 1
                if count == frames:
                    count = 0
                anim = root.after(50, lambda: animation(count))
            except:
                pass
        
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
            try:
                gif_label.configure(image=im2)
                count += 1
                if count == frames:
                    count = 0
                anim = root.after(50, lambda: animation(count))
            except:
                pass
        
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
        if self.background_image is not None:
            self.background_image.destroy()
        self.background_image = Label(self, image=render, borderwidth = 0)
        self.background_image.image = render
        self.background_image.place(x=0, y=0)

    def loadEnemy(self, fileName, health):
        gif = Image.open(fileName)
        frames = gif.n_frames
        im = [PhotoImage(file=fileName,format=f"gif -index {i}") for i in range(frames)]
        count = 0
        anim = None

        def animation(count):
            global anim
            im2 = im[count]
            try:
                gif_label.configure(image=im2)
                count += 1
                if count == frames:
                    count = 0
                anim = root.after(50,lambda :animation(count))
            except:
                pass
        
        label = Label(self, text=str(health))
        label.pack(side=RIGHT, anchor=SE)
        label.configure(bg='black', fg='white')
        gif_label = Label(self,image="", width=115, height=115)
        gif_label.pack(side=RIGHT, anchor=SE)
        gif_label.configure(bg='black', fg='white')
        self.enemies.append(EnemyDisplay(label, gif_label, self))
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

class EnemyDisplay():
    def __init__(self, health_label:Label, gif_label:Label, app:Window):
        self.health_label = health_label
        self.gif_label = gif_label
        self.app = app

    def destroy(self):
        self.health_label.destroy()
        self.gif_label.destroy()

    def set_health(self, hp):
        self.health_label.config(text=str(hp))


    def deal_damage(self, dmg):
        health = int(self.health_label.cget("text"))
        health -= dmg
        if health > 0:
            self.health_label.config(text = str(health))
            return True
        else:
            return False

def kill_enemies_after_time(time_s, app:Window):
    while True:
        inp = input("index and dmg: ")
        index, dmg = [int(i) for i in inp.split()]
        app.harm_enemy(index, dmg)

if __name__ == "__main__":
    root = Tk()
    app = Window(root)
    root.wm_title("Background")
    root.geometry("800x480")
    app.loadImage("guiPics/dungeon_three.jpeg")
    app.drinkPotion("guiPics/potion5.gif")
    app.loadBlade("guiPics/blade.gif")
    app.loadEnemy("guiPics/orc.gif", 1)
    app.loadEnemy("guiPics/slime.gif", 2)
    app.loadEnemy("guiPics/demon.gif", 3)
    app.loadKey("guiPics/key.jpeg")
    app.healthBar(100)

    thread = threading.Thread(target=kill_enemies_after_time, args=[5, app])
    thread.start()
    root.mainloop()
