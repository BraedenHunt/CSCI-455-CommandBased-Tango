import tkinter as tk

import PIL
from PIL.Image import Image

from DriveCommand import DriveCommand
from RobotContainer import RobotContainer
from SayPhraseCommand import SayPhraseCommand
from ServoCommand import ServoCommand
from WaitForPhraseCommand import WaitForPhraseCommand


class RobotGUI(tk.Tk):
    def __init__(self, robot_container : RobotContainer, master=None):
        tk.Tk.__init__(self,master)
        self.robot_container = robot_container
        self.actCnt = 1
        self.rowCnt = 0
        self.colCnt = 0
        self.actions = []
        self.commands = self.robot_container.command_queue
        self.actionWidgets = []
        self.grid()
        self.createLayout()

    def createLayout(self):
        self.frm_timeline = tk.Frame(self, bd=2,bg="black", highlightbackground="white", highlightthickness=1)


        self.frm_buttons = tk.Frame(self, relief=tk.RAISED, bd=2, bg="black")
        self.btn_start = tk.Button(self.frm_buttons,bg="grey",fg="white", text="Start", command=lambda: self.start())

        self.btn_drive = tk.Button(self.frm_buttons, text="Drive",bg="grey",fg="light blue", command=lambda: self.placeAction("Drive"))
        self.btn_turn = tk.Button(self.frm_buttons,bg="grey",fg="light blue", text="Turn", command=lambda: self.placeAction("Turn"))
        self.btn_pitchHead = tk.Button(self.frm_buttons,bg="grey",fg="light blue", text="Pitch Head", command=lambda: self.placeAction("Pitch"))
        self.btn_rollHead = tk.Button(self.frm_buttons,bg="grey",fg="light blue", text="Roll Head", command=lambda: self.placeAction("Roll"))
        self.btn_rotTorso = tk.Button(self.frm_buttons,bg="grey",fg="light blue", text="Rotate Torso", command=lambda: self.placeAction("Torso"))
        self.btn_waitForVoice = tk.Button(self.frm_buttons,bg="grey",fg="light blue", text="Wait for Speech", command=lambda: self.placeAction("Hear"))
        self.btn_speak = tk.Button(self.frm_buttons,bg="grey",fg="light blue", text="Speak", command=lambda: self.placeAction("Speak"))

        self.btn_reset = tk.Button(self.frm_buttons,bg="grey",fg="orange", text="Reset", command=lambda:self.reset())
        self.btn_close = tk.Button(self.frm_buttons, text="Close",bg="grey",fg="red", command=lambda: self.destroy())

        self.btn_start.grid(row=0, column=0,sticky="ew",padx=5,pady=(5,50))

        self.btn_drive.grid(row=1, column=0,sticky="ew",padx=5,pady=5)
        self.btn_turn.grid(row=2, column=0,sticky="ew",padx=5,pady=5)
        self.btn_pitchHead.grid(row=3, column=0,sticky="ew",padx=5,pady=5)
        self.btn_rollHead.grid(row=4, column=0,sticky="ew",padx=5,pady=5)
        self.btn_rotTorso.grid(row=5, column=0,sticky="ew",padx=5,pady=5)
        self.btn_waitForVoice.grid(row=6, column=0,sticky="ew",padx=5,pady=5)
        self.btn_speak.grid(row=7, column=0,sticky="ew",padx=5,pady=5)

        self.btn_reset.grid(row=8, column=0, sticky="ew", padx=5,pady=5)
        self.btn_close.grid(row=9, column=0, sticky="ew", padx=5,pady=5)



        self.frm_gif = tk.Frame(self, relief=tk.RAISED, bd=2, bg="blue")


        self.openAnimation()


        self.frm_buttons.grid(row=0, column=0, sticky="ns")
        self.frm_timeline.grid(row=0, column=1, sticky="nsew")
        self.frm_gif.grid(row=1, column=1, sticky="nsew")


    def start(self):
        if(self.actions):
            self.commands.queue.clear()
            print("Starting:")
            for action in self.actions:
                if isinstance(action, Drive):
                    command = DriveCommand(self.robot_container.drivetrain, action.dur/1000.0, action.dir * action.spd/6.0, action.dir * action.spd/6.0)

                elif isinstance(action, Turn):
                    command = DriveCommand(self.robot_container.drivetrain, action.dur/1000.0, -1 * action.dir * action.spd / 6.0,
                                           action.dir * action.spd / 6.0)
                elif isinstance(action, Hear):
                    command = WaitForPhraseCommand(self.robot_container.speech_listener, action.listenFor)
                elif isinstance(action, Speak):
                    command = SayPhraseCommand(self.robot_container.speaker,action.say)
                elif isinstance(action, Roll):
                    command = ServoCommand(self.robot_container.head_twist, action.pos/2.0)
                elif isinstance(action, Torso):
                    command = ServoCommand(self.robot_container.waist, action.pos/2.0)
                elif isinstance(action, Pitch):
                    command = ServoCommand(self.robot_container.head_tilt, -action.pos/2.0)
                else:
                    print("Unknown action: " + action)
                self.commands.put(command)
                action.print()
            print("Finished.")
            return
        print("No commands in timeline.")

    def reset(self):
        for actionWidget in self.actionWidgets:
            actionWidget.destroy()
        self.actions = []
        self.actionWidgets = []
        self.actCnt=1
        self.colCnt=0
        self.rowCnt=0

    def placeAction(self,title):

        if(self.actCnt>18):
            top=tk.Toplevel(self)
            top.title("Error")
            tk.Label(top, text="18 Action Commands is the Maximum.",bg="grey", fg="yellow", font=("Helvetica 20 bold")).pack()
            return

        if(title=="Drive"):
            widget=self.createDrive()
        elif(title=="Turn"):
            widget=self.createTurn()
        elif(title=="Pitch"):
            widget=self.createPitch()
        elif(title=="Roll"):
            widget=self.createRoll()
        elif(title=="Torso"):
            widget=self.createTorso()
        elif(title=="Hear"):
            widget=self.createHear()
        elif(title=="Speak"):
            widget=self.createSpeak()
        
        self.actCnt+=1
        self.colCnt+=1
        if(self.colCnt==3):
            self.colCnt = 0
            self.rowCnt += 1

    def createDrive(self):
        action = Drive()
        widget = action.createLayout(self.frm_timeline,self.actCnt)
        widget.grid(row=self.rowCnt, column=self.colCnt, sticky="nsew",pady=10,padx=2)
        self.actionWidgets.append(widget)
        self.actions.append(action)

    def createTurn(self):
        action = Turn()
        widget = action.createLayout(self.frm_timeline,self.actCnt)
        widget.grid(row=self.rowCnt, column=self.colCnt, sticky="nsew",pady=10,padx=2)
        self.actionWidgets.append(widget)
        self.actions.append(action)


    def createPitch(self):
        action = Pitch()
        widget = action.createLayout(self.frm_timeline,self.actCnt)
        widget.grid(row=self.rowCnt, column=self.colCnt, sticky="nsew",pady=10,padx=2)
        self.actionWidgets.append(widget)
        self.actions.append(action)

    def createRoll(self):
        action = Roll()
        widget = action.createLayout(self.frm_timeline,self.actCnt)
        widget.grid(row=self.rowCnt, column=self.colCnt, sticky="nsew",pady=10,padx=2)
        self.actionWidgets.append(widget)
        self.actions.append(action)

    def createTorso(self):
        action = Torso()
        widget = action.createLayout(self.frm_timeline,self.actCnt)
        widget.grid(row=self.rowCnt, column=self.colCnt, sticky="nsew",pady=10,padx=2)
        self.actionWidgets.append(widget)
        self.actions.append(action)

    def createHear(self):
        action = Hear()
        widget = action.createLayout(self.frm_timeline,self.actCnt)
        widget.grid(row=self.rowCnt, column=self.colCnt, sticky="nsew",pady=10,padx=2)
        self.actionWidgets.append(widget)
        self.actions.append(action)

    def createSpeak(self):
        action = Speak()
        widget = action.createLayout(self.frm_timeline,self.actCnt)
        widget.grid(row=self.rowCnt, column=self.colCnt, sticky="nsew",pady=10,padx=2)
        self.actionWidgets.append(widget)
        self.actions.append(action)

    def openAnimation(self):
        self.animation_window = tk.Toplevel(self)
        self.animation_window.title("Animation")
        self.animation_window.geometry("304x304")
        self.file = "robot_eyes.gif"
        self.info = PIL.Image.open(self.file)

        self.frames = self.info.n_frames
        self.im = [tk.PhotoImage(file=self.file, format=f"gif -index {i}") for i in range(self.frames)]

        self.count = 0
        self.anim = None
        self.gif_label = tk.Label(self.animation_window, image="")
        self.gif_label.pack()
        self.animation_window.geometry("480x480")


        self.animation_window.grab_set()
        self.animation()

    def animation(self):
        im2 = self.im[self.count]

        self.gif_label.configure(image=im2)
        self.count += 1
        if self.count == self.frames:
            self.count = 0
        self.anim = self.after(50,lambda :self.animation())

#Action Objects
class Drive():
    def __init__(self):
        self.options = None
        self.dir = 1;
        self.dur = 1000;
        self.spd = 3;

    def createLayout(self,parentFrame,count):
        actionTitle = "#%d. Drive" % (count)  
        
        frm = tk.Frame(parentFrame,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
           
        lbl=tk.Label(frm,text=actionTitle,bg="black",fg="white",height=2,width=15)
        lbl.grid(column=0, row=0)

        btn = tk.Button(frm,text="Edit",fg="white",bg="grey",highlightbackground="light grey",height=2,width=5,command=lambda: self.openOptions())
        btn.grid(column=1,row=0)

        return frm

    def print(self):
        print("Driving with direction %d, at speed %d, for %dms" % (self.dir, self.spd, self.dur))

    def openOptions(self):
        self.options = tk.Tk()
        self.options.title("Drive Options")
        self.options.geometry("360x140")
        
        frm = tk.Frame(self.options,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
        frm.grid(column=0, row=0, sticky="nesw")

        dirLbl=tk.Label(frm,text="Direction:",bg="black",fg="white",height=2,width=15)
        dirLbl.grid(column=0, row=0,sticky="w")

        direction = tk.IntVar(frm,self.dir)
        r1 = tk.Radiobutton(frm,text="Forward", value=1,variable=direction,fg="white",bg="black",highlightbackground="light grey",selectcolor="grey")
        r2 = tk.Radiobutton(frm,text="Backwards", value=-1,fg="white",variable=direction,bg="black",highlightbackground="light grey",selectcolor="grey")
        r1.grid(column=0,row=1,sticky="w")
        r2.grid(column=0,row=2,sticky="w")

        spdLbl=tk.Label(frm,text="Speed:",bg="black",fg="white",height=2,width=15)
        spdLbl.grid(column=1, row=0,sticky="w", padx=5)

        speed = tk.IntVar(frm,self.spd)
        sr1 = tk.Radiobutton(frm,text="Slow", value=3,variable=speed,fg="white",bg="black",highlightbackground="light grey",selectcolor="grey")
        sr2 = tk.Radiobutton(frm,text="Medium", value=4,fg="white",variable=speed,bg="black",highlightbackground="light grey",selectcolor="grey")
        sr3 = tk.Radiobutton(frm,text="Fast", value=6,fg="white",variable=speed,bg="black",highlightbackground="light grey",selectcolor="grey")
        sr1.grid(column=1,row=1,sticky="w")
        sr2.grid(column=1,row=2,sticky="w")
        sr3.grid(column=1,row=3,sticky="w")

        durLbl=tk.Label(frm,text="Duration(ms):",bg="black",fg="white",height=2,width=15)
        durLbl.grid(column=2, row=0,sticky="w", padx=5)

        duration = tk.StringVar(frm,self.dur)
        durEntry = tk.Entry(frm, fg="white",bg="black",highlightbackground="light grey", textvariable=duration)
        durEntry.grid(column=2,row=1,sticky="w")
        
        btn = tk.Button(frm,text="Save and Close",fg="white",bg="grey",highlightbackground="light grey",command=lambda: self.saveAndClose(direction.get(),speed.get(),int(duration.get())))
        btn.grid(column=1,row=4,sticky="w")


    def saveAndClose(self,direction,speed,duration):
        self.dir = direction
        self.spd = speed
        self.dur = duration
        self.options.destroy()
        self.options = None

class Turn():
    def __init__(self):
        self.dir = 1;
        self.dur = 1000;
        self.spd = 3;
    
    def createLayout(self,parentFrame,count):
        actionTitle = "#%d. Turn" % (count)  
        
        frm = tk.Frame(parentFrame,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
           
        lbl=tk.Label(frm,text=actionTitle,bg="black",fg="white",height=2,width=15)
        lbl.grid(column=0, row=0)

        btn = tk.Button(frm,text="Edit",fg="white",bg="grey",highlightbackground="light grey",height=2,width=5,command=lambda: self.openOptions())
        btn.grid(column=1,row=0)

        return frm

    def print(self):
        print("Turning with direction %d, at speed %d, for %dms" % (self.dir, self.spd, self.dur))

    def openOptions(self):
        self.options = tk.Tk()
        self.options.title("Turn Options")
        self.options.geometry("360x140")
        
        frm = tk.Frame(self.options,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
        frm.grid(column=0, row=0, sticky="nesw")

        dirLbl=tk.Label(frm,text="Direction:",bg="black",fg="white",height=2,width=15)
        dirLbl.grid(column=0, row=0,sticky="w")

        direction = tk.IntVar(frm,self.dir)
        r1 = tk.Radiobutton(frm,text="left", value=-1,variable=direction,fg="white",bg="black",highlightbackground="light grey",selectcolor="grey")
        r2 = tk.Radiobutton(frm,text="right", value=1,fg="white",variable=direction,bg="black",highlightbackground="light grey",selectcolor="grey")
        r1.grid(column=0,row=1,sticky="w")
        r2.grid(column=0,row=2,sticky="w")

        spdLbl=tk.Label(frm,text="Speed:",bg="black",fg="white",height=2,width=15)
        spdLbl.grid(column=1, row=0,sticky="w", padx=5)

        speed = tk.IntVar(frm,self.spd)
        sr1 = tk.Radiobutton(frm,text="Slow", value=3,variable=speed,fg="white",bg="black",highlightbackground="light grey",selectcolor="grey")
        sr2 = tk.Radiobutton(frm,text="Medium", value=4,fg="white",variable=speed,bg="black",highlightbackground="light grey",selectcolor="grey")
        sr3 = tk.Radiobutton(frm,text="Fast", value=6,fg="white",variable=speed,bg="black",highlightbackground="light grey",selectcolor="grey")
        sr1.grid(column=1,row=1,sticky="w")
        sr2.grid(column=1,row=2,sticky="w")
        sr3.grid(column=1,row=3,sticky="w")

        durLbl=tk.Label(frm,text="Duration(ms):",bg="black",fg="white",height=2,width=15)
        durLbl.grid(column=2, row=0,sticky="w", padx=5)

        duration = tk.StringVar(frm,self.dur)
        durEntry = tk.Entry(frm, fg="white",bg="black",highlightbackground="light grey", textvariable=duration)
        durEntry.grid(column=2,row=1,sticky="w")
        
        btn = tk.Button(frm,text="Save and Close",fg="white",bg="grey",highlightbackground="light grey",command=lambda: self.saveAndClose(direction.get(),speed.get(),int(duration.get())))
        btn.grid(column=1,row=4,sticky="w")


    def saveAndClose(self,direction,speed,duration):
        self.dir = direction
        self.spd = speed
        self.dur = duration
        self.options.destroy()
        self.options = None

class Pitch():
    def __init__(self):
        self.pos = 0

    def createLayout(self,parentFrame,count):
        actionTitle = "#%d. Pitch Head"% (count)  
        
        frm = tk.Frame(parentFrame,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
           
        lbl=tk.Label(frm,text=actionTitle,bg="black",fg="white",height=2,width=15)
        lbl.grid(column=0, row=0)

        btn = tk.Button(frm,text="Edit",fg="white",bg="grey",highlightbackground="light grey",height=2,width=5, command = lambda: self.openOptions())
        btn.grid(column=1,row=0)

        return frm

    def print(self):
        print("Pitching head to position %d" % (self.pos))

    def openOptions(self):
        self.options = tk.Tk()
        self.options.title("Pitch Head Options")
        self.options.geometry("110x210")
        
        frm = tk.Frame(self.options,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
        frm.grid(column=0, row=0, sticky="nesw")

        posLbl=tk.Label(frm,text="Head Pitch:",bg="black",fg="white",height=2,width=15)
        posLbl.grid(column=0, row=0,sticky="w", padx=5)

        position = tk.IntVar(frm,self.pos)
        pr1 = tk.Radiobutton(frm,text="Far Down", value=-2,variable=position,fg="white",bg="black",highlightbackground="light grey",selectcolor="grey")
        pr2 = tk.Radiobutton(frm,text="Down", value=-1,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr3 = tk.Radiobutton(frm,text="Middle", value=0,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr4 = tk.Radiobutton(frm,text="Up", value=1,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr5 = tk.Radiobutton(frm,text="Far Up", value=2,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr1.grid(column=0,row=1,sticky="w")
        pr2.grid(column=0,row=2,sticky="w")
        pr3.grid(column=0,row=3,sticky="w")
        pr4.grid(column=0,row=4,sticky="w")
        pr5.grid(column=0,row=5,sticky="w")
        
        btn = tk.Button(frm,text="Save and Close",fg="white",bg="grey",highlightbackground="light grey",command=lambda: self.saveAndClose(position.get()))
        btn.grid(column=0,row=6,sticky="w",pady=(15,5))


    def saveAndClose(self,position):
        self.pos = position
        self.options.destroy()
        self.options = None


class Roll():
    def __init__(self):
        self.pos = 0
    
    def createLayout(self,parentFrame,count):
        actionTitle = "#%d. Roll Head" % (count)  
        
        frm = tk.Frame(parentFrame,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
           
        lbl=tk.Label(frm,text=actionTitle,bg="black",fg="white",height=2,width=15)
        lbl.grid(column=0, row=0)

        btn = tk.Button(frm,text="Edit",fg="white",bg="grey",highlightbackground="light grey",height=2,width=5, command=lambda: self.openOptions())
        btn.grid(column=1,row=0)

        return frm

    def print(self):
        print("Rolling head to position %d" % (self.pos))

    def openOptions(self):
        self.options = tk.Tk()
        self.options.title("Roll Head Options")
        self.options.geometry("110x210")
        
        frm = tk.Frame(self.options,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
        frm.grid(column=0, row=0, sticky="nesw")

        posLbl=tk.Label(frm,text="Head Roll:",bg="black",fg="white",height=2,width=15)
        posLbl.grid(column=0, row=0,sticky="w", padx=5)

        position = tk.IntVar(frm,self.pos)
        pr1 = tk.Radiobutton(frm,text="Far Left", value=-2,variable=position,fg="white",bg="black",highlightbackground="light grey",selectcolor="grey")
        pr2 = tk.Radiobutton(frm,text="Left", value=-1,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr3 = tk.Radiobutton(frm,text="Middle", value=0,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr4 = tk.Radiobutton(frm,text="Right", value=1,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr5 = tk.Radiobutton(frm,text="Far Right", value=2,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr1.grid(column=0,row=1,sticky="w")
        pr2.grid(column=0,row=2,sticky="w")
        pr3.grid(column=0,row=3,sticky="w")
        pr4.grid(column=0,row=4,sticky="w")
        pr5.grid(column=0,row=5,sticky="w")
        
        btn = tk.Button(frm,text="Save and Close",fg="white",bg="grey",highlightbackground="light grey",command=lambda: self.saveAndClose(position.get()))
        btn.grid(column=0,row=6,sticky="w",pady=(15,5))


    def saveAndClose(self,position):
        self.pos = position
        self.options.destroy()
        self.options = None

class Torso():
    def __init__(self):
        self.pos = 0;

    def createLayout(self,parentFrame,count):
        actionTitle = "#%d. Rotate Torso" % (count)  
        
        frm = tk.Frame(parentFrame,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
           
        lbl=tk.Label(frm,text=actionTitle,bg="black",fg="white",height=2,width=15)
        lbl.grid(column=0, row=0)

        btn = tk.Button(frm,text="Edit",fg="white",bg="grey",highlightbackground="light grey",height=2,width=5, command=lambda: self.openOptions())
        btn.grid(column=1,row=0)

        return frm

    def print(self):
        print("Rotating Torso to position %d" % (self.pos))

    def openOptions(self):
        self.options = tk.Tk()
        self.options.title("Rotate Torso Options")
        self.options.geometry("110x160")
        
        frm = tk.Frame(self.options,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
        frm.grid(column=0, row=0, sticky="nesw")

        posLbl=tk.Label(frm,text="Torso Rotation:",bg="black",fg="white",height=2,width=15)
        posLbl.grid(column=0, row=0,sticky="w", padx=5)

        position = tk.IntVar(frm,self.pos)
        pr1 = tk.Radiobutton(frm,text="Left", value=-1,variable=position,fg="white",bg="black",highlightbackground="light grey",selectcolor="grey")
        pr2 = tk.Radiobutton(frm,text="Middle", value=0,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr3 = tk.Radiobutton(frm,text="Right", value=1,fg="white",variable=position,bg="black",highlightbackground="light grey",selectcolor="grey")
        pr1.grid(column=0,row=1,sticky="w")
        pr2.grid(column=0,row=2,sticky="w")
        pr3.grid(column=0,row=3,sticky="w")
        
        btn = tk.Button(frm,text="Save and Close",fg="white",bg="grey",highlightbackground="light grey",command=lambda: self.saveAndClose(position.get()))
        btn.grid(column=0,row=4,sticky="w",pady=(15,5))


    def saveAndClose(self,position):
        self.pos = position
        self.options.destroy()
        self.options = None

class Hear():
    def __init__(self):
        self.listenFor = "hello"
    
    def createLayout(self,parentFrame,count):
        actionTitle = "#%d. Wait for Voice" % (count)  
        
        frm = tk.Frame(parentFrame,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
           
        lbl=tk.Label(frm,text=actionTitle,bg="black",fg="white",height=2,width=15)
        lbl.grid(column=0, row=0)

        btn = tk.Button(frm,text="Edit",fg="white",bg="grey",highlightbackground="light grey",height=2,width=5, command = lambda: self.openOptions())
        btn.grid(column=1,row=0)

        return frm

    def print(self):
        print("Waiting to hear \"%s\"" % (self.listenFor))

    def openOptions(self):
        self.options = tk.Tk()
        self.options.title("Wait for Voice Options")
        self.options.geometry("130x105")
        
        frm = tk.Frame(self.options,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
        frm.grid(column=0, row=0, sticky="nesw")

        hearLbl=tk.Label(frm,text="Listen For:",bg="black",fg="white",height=2,width=15)
        hearLbl.grid(column=0, row=0,sticky="w", padx=5)

        listen = tk.StringVar(frm,self.listenFor)
        durEntry = tk.Entry(frm, fg="white",bg="black",highlightbackground="light grey", textvariable=listen)
        durEntry.grid(column=0,row=1,sticky="w")
        
        btn = tk.Button(frm,text="Save and Close",fg="white",bg="grey",highlightbackground="light grey",command=lambda: self.saveAndClose(listen.get()))
        btn.grid(column=0,row=2,sticky="w",pady=(15,5))


    def saveAndClose(self,listen):
        self.listenFor = listen
        self.options.destroy()
        self.options = None

class Speak():
    def __init__(self):
        self.say="Hello World"

    def createLayout(self,parentFrame,count):
        actionTitle = "#%d. Speak" % (count)  
        
        frm = tk.Frame(parentFrame,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
           
        lbl=tk.Label(frm,text=actionTitle,bg="black",fg="white",height=2,width=15)
        lbl.grid(column=0, row=0)

        btn = tk.Button(frm,text="Edit",fg="white",bg="grey",highlightbackground="light grey",height=2,width=5, command = lambda: self.openOptions())
        btn.grid(column=1,row=0)

        return frm

    def print(self):
        print("Speaking: \"%s\" " % (self.say))

    def openOptions(self):
        self.options = tk.Tk()
        self.options.title("Speak Options")
        self.options.geometry("130x105")
        
        frm = tk.Frame(self.options,bd=2,highlightbackground="white", highlightthickness=1,bg="black")
        frm.grid(column=0, row=0, sticky="nesw")

        sayLbl=tk.Label(frm,text="Say:",bg="black",fg="white",height=2,width=15)
        sayLbl.grid(column=0, row=0,sticky="w", padx=5)

        say = tk.StringVar(frm,self.say)
        durEntry = tk.Entry(frm, fg="white",bg="black",highlightbackground="light grey", textvariable=say)
        durEntry.grid(column=0,row=1,sticky="w")
        
        btn = tk.Button(frm,text="Save and Close",fg="white",bg="grey",highlightbackground="light grey",command=lambda: self.saveAndClose(say.get()))
        btn.grid(column=0,row=2,sticky="w",pady=(15,5))


    def saveAndClose(self,say):
        self.say = say
        self.options.destroy()
        self.options = None


##############################################################
# MAIN LOOP
if __name__ == "__main__":
    window = RobotGUI()
    window.title("Robot Control GUI")
    window.rowconfigure(0, minsize=480, weight=1)
    window.columnconfigure(1,minsize=800,weight=1)
    window.geometry("800x480")
    window.mainloop()

##############################################################
# NOTES
#
# Properties of the commands are accessed via the list of actions in the window.
# Right now the start button is configured to print them.
#
# For drive:
#   dir: Forward = 1, backwards = 0
#   spd: Speed = 1,2, or 3
#   dur: Duration = time in ms
#
# For turn
#   dir: left = 1, right = 0
#   spd: speed = 1,2, or 3
#   dur: Duration = time in ms
#
# For pitch
#   pos: position of the head pitch, ranges from -2 to 2, negative side being down
#
# For Roll
#   pos: position of the head roll, ranges from -2 to 2, negative side being the robot's left
#
# For Torso Rotation
#   pos: position of the robot's torso rotation, ranges from -1 to 1, negative side being the robot's left
#
# For Wait for voice
#   listen: the word or phrase the robot is listening for, in string form
#
# For Speak
#   say: the phrase the robot is going to speak, in string form
#
