import random
import os
import sys
from queue import Queue

from DriveCommand import DriveCommand
from ListenCommand import ListenCommand
from RobotContainer import RobotContainer
from SayPhraseCommand import SayPhraseCommand
from robot_animations import Window

rb_container: RobotContainer = None
app : Window = None
startDesc = "You awake in an empty dungeon cell... how will you escape?\nBeware, as you only have limited time to make it out!"

startRoomDesc = "An empty cell, you started here."

endRoomDesc = "There is a massive locked door that blocks the way out."

timeLoseText = "Succumbing to fatigue, you collapse. OUT OF TIME: YOU HAVE FAILED"

monsterLoseText = "The monster strikes a fatal blow! YOU HAVE FAILED"

trapLoseText = "The deadly trap has been your doom! YOU HAVE FAILED"

winText = "The key turns in the door, opening the way to freedom. YOU WIN"

roomIntros = [
    "You see ",
    "Here, there is ",
    "Ahead you can see ",
    "Looming up ahead, ",
    "You find ",
    "The next room is ",
    "There is ",
    "You find yourself at "
]

roomDescs = [
    "a dusty, torchlit hallway.",
    "a large, pillared throne room.",
    "an echoing, dark cavern.",
    "a grimey, torchlit cell.",
    "a dank and moldy vault.",
    "some slippery steps leading down.",
    "a chilled, swampy chasm.",
    "a high-ceilinged, echoing chapel.",
    "a grim, candle-lit ossuary.",
    "a reeking, refuse-strewn cesspit.",
    "an imposing bastion of blackened iron.",
    "a ruined heap of crumbled marble.",
    "a long-abandoned workshop of tarnished brass.",
    "a papery-walled, buzzing insect hive.",
    "a cramped, malodorous burrow.",
    "a lonely, lofted bridge of narrow brick.",
    "a great, yawning pit.",
    "a room filled with rugs of every color.",
    "a courtyard of flickering candles.",
    "a twisting hall of mirrors.",
    "an abandoned bakery that still smells of bread.",
    "a domed chamber painted with stars.",
    "a frightening portrait gallery.",
    "a decrepit catacomb, filled with bones",
    "an old dungeon, skeletons hanging from shackles",
    "a set of uneven steps, leading upwards.",
    "a grand cathedral with ornate pillars.",
    "a dimly lit circular room with many doors",
    "a well lit entryway with colorful tiled floors",
    "a neverending tunnel with red lanterns",
    "a dazzling open room filled with exquisite pews",
    "a hazy crawlspace with slimy floors",
    "a musty archive filled with old papers."
]

adventureMap = [
    {   #room 1
        'east':2
    },
    {   #room 2
        'south':7,
        'east':3,
        'west':1
    },
    {   #room 3
        'south':8,
        'west':2
    },
    {   #room 4
        'east':5
    },
    {   #room 5
        'west':4,
        'south':10
    },
    {   #room 6
        'east':7,
        'south':11
    },
    {   #room 7
        'north':2,
        'west':6,
        'south':12
    },
    {   #room 8
        'north':3
    },
    {   #room 9
        'east':10,
        'south':14
    },
    {   #room 10
        'north':5,
        'west':9,
        'south':15
    },
    {   #room 11
        'north':6,
        'south':16
    },
    {   #room 12
        'north':7,
        'east':13
    },
    {   #room 13
        'east':14,
        'west':12
    },
    {   #room 14
        'west':13,
        'north':9,
        'south':19
    },
    {   #room 15
        'north':10,
        'south':20
    },
    {   #room 16
        'north':11,
        'east':17
    },
    {   #room 17
        'west':16,
        'south':22
    },
    {   #room 18
        'south':23
    },
    {   #room 19
        'north':14,
        'south':24,
        'east':20
    },
    {   #room 20
        'west':19,
        'north':15
    },
    {   #room 21
        'east':22
    },
    {   #room 22
        'west':21,
        'north':17,
        'east':23
    },
    {   #room 23
        'west':22,
        'north':18
    },
    {   #room 24
        'east':25,
        'north':19
    },
    {   #room 25
        'west':24
    }
]

###############################################################################################
# Classes
###############################################################################################
class Node():
    def __init__(self, *args):
        if len(args) == 2:
            self.loc=args[0]        # contains the interger room
            self.desc=None          # contains the text description of the room, later may contain some Tkinter display info
            self.content = args[1]  # can contain start, finish, Encounter, charging station, wifi, riddle, or Other
            self.getDesc()
        else:
            self.loc=args[0]        # contains the interger room
            self.desc=args[2]       # contains the text description of the room, later may contain some Tkinter display info
            self.content=args[1]    # can contain start, finish, Encounter, charging station, wifi, riddle, or other  


    def getDesc(self):
        text = roomDescs[random.randint(0,len(roomDescs)-1)]
        roomDescs.remove(text)
        introText = roomIntros[random.randint(0,len(roomIntros)-1)]
        self.desc = introText + text

class Knight():
    def __init__(self):
        self.hp=100         # hit points
        app.healthBar(100)
        self.key=False      # do you have the key?
        self.sword=False    # do you have the magic sword
        self.potion=0       # what potion do you have

    def attack(self, target):
        mult = 1
        if self.sword:
            mult = 3
        dmg = mult * random.randint(0,8)
        if dmg==0:
            say("Oh no, you missed!")
        else:
            say("You hit the " + target + " for " + str(dmg) + " damage!")
        return dmg


class Start():
    def __repr__(cls):
        return 'Start'
    def act(self,knight):
        return
    
class Finish():
    def __repr__(cls):
        return 'Finish'
    def act(self,knight):
        if knight.key:
            say("Luckily, you have the key!")
            return True
        else:
            say("Looks like you need a key.")
            return False

class Other():
    def __repr__(cls):
        return 'Other'

    def __init__(self):
        self.type = random.randint(1,5)
        self.used = False
    
    def act(self,knight):
        if(not self.used):
            answer = speech_input("Something is off about this room, investigate? [y/n]: ")
            if answer == 'n':
                return
            else:
                if self.type == 1:
                    say("You find a magical blade, glowing with power! It will help you fight monsters.")
                    knight.sword = True
                    #TODO add sword
                elif self.type > 1 and self.type < 5:
                    say("You find a bottle filled with a swirling liquid, a potion! When not fighting, type 'potion' to use.\n But beware, who knows what it does!")
                    knight.potion+=1
                    #TODO add potion

                else:
                    dmg = random.randint(5,15)
                    say("You spring a hidden trap! The swinging blade hits you for " + str(dmg) + " damage!")
                    knight.hp -= dmg
                    # TODO trapped room
                    if knight.hp <= 0:
                        say(trapLoseText)
                        playAgain()
                self.used = True           
        else:
            say("There is nothing else to find here.")

class Recharge():
    def __repr__(cls):
        return 'Recharge'
    
    def __init__(self):
        self.used = False
        
    def act(self,knight):
        if(not self.used):
            if knight.hp == 100:
                say("Magic runes carved here could refill your health, if you were hurt.")
                return
            else:
                knight.hp = 100
                # TODO Update health
                app.healthBar(100)
                say("The magic runes carved here refill your health")
                self.used = True
        else:
            say("The magic runes here have been used.")

class Key():
    def __repr__(cls):
        return 'Key'

    def __init__(self):
        self.used = False
        self.solution = random.randint(0,1)
    
    def act(self,knight):
        if(not self.used):
            say("A golden chest sits in the center of this room, carved with a square and a triangle.")
            if self.solution:
                say("A riddle reads: The number of musketeers is the key.")
            else:
                say("A riddle reads: The turning of the seasons reveals the key")

            choice = speech_input("What do you choose? [square, triangle, leave]: ")

            if choice == 'square':
                numChoice = 0
            elif choice == 'triangle':
                numChoice = 1
            elif choice == 'leave':
                return
            else:
                say("That is not a valid choice, come back later")
                return

            if numChoice == self.solution:
                say("At the press of the button, the chest opens, revealing a key!")
                knight.key = True
            else:
                    dmg = random.randint(15,50)
                    say("The wrong choice! A poison needle jabs you for " + str(dmg) + " damage!\nPressing the other button, you find a key.")
                    knight.key = True
                    knight.hp -= dmg
                    #TODO update health
                    if knight.hp <= 0:
                        say(trapLoseText)
                        playAgain()
            #TODO add key
            self.used = True           
        else:
            say("There is nothing else to find here.")

class Hint():
    def __repr__(cls):
        return 'Hint'
    
    def act(self,knight,curRoomNum,endRoomNum):
        curRoomCoord = self.getCoord(curRoomNum)
        endRoomCoord = self.getCoord(endRoomNum)

        if (curRoomCoord[0] == endRoomCoord[0]) and (curRoomCoord[1] > endRoomCoord[1]):
            hint = "north"
        elif (curRoomCoord[0] < endRoomCoord[0]) and (curRoomCoord[1] > endRoomCoord[1]):
            hint = "northeast"
        elif (curRoomCoord[0] < endRoomCoord[0]) and (curRoomCoord[1] == endRoomCoord[1]):
            hint = "east"
        elif (curRoomCoord[0] < endRoomCoord[0]) and (curRoomCoord[1] < endRoomCoord[1]):
            hint = "southeast"
        elif (curRoomCoord[0] == endRoomCoord[0]) and (curRoomCoord[1] < endRoomCoord[1]):
            hint = "south"
        elif (curRoomCoord[0] > endRoomCoord[0]) and (curRoomCoord[1] < endRoomCoord[1]):
            hint = "southwest"
        elif (curRoomCoord[0] > endRoomCoord[0]) and (curRoomCoord[1] == endRoomCoord[1]):
            hint = "west"
        elif (curRoomCoord[0] > endRoomCoord[0]) and (curRoomCoord[1] > endRoomCoord[1]):
            hint = "northwest"
        
        say("A cryptic message points the way: the exit is " + hint + " of here.")

    def getCoord(self,num):
        if num == 1:
            return [0,0]
        elif num == 2:
            return [1,0]
        elif num == 3:
            return [2,0]
        elif num == 4:
            return [3,0]
        elif num == 5:
            return [4,0]
        elif num == 6:
            return [0,1]
        elif num == 7:
            return [1,1]
        elif num == 8:
            return [2,1]
        elif num == 9:
            return [3,1]
        elif num == 10:
            return [4,1]
        elif num == 11:
            return [0,2]
        elif num == 12:
            return [1,2]
        elif num == 13:
            return [2,2]
        elif num == 14:
            return [3,2]
        elif num == 15:
            return [4,2]
        elif num == 16:
            return [0,3]
        elif num == 17:
            return [1,3]
        elif num == 18:
            return [2,3]
        elif num == 19:
            return [3,3]
        elif num == 20:
            return [4,3]
        elif num == 21:
            return [0,4]
        elif num == 22:
            return [1,4]
        elif num == 23:
            return [2,4]
        elif num == 24:
            return [3,4]
        elif num == 25:
            return [4,4]

    
class Encounter():
    def __repr__(cls):
        return 'Encounter'
    
    def __init__(self,difficulty):
        self.enemies = []       # what enemies there are (holds objects)
        app.enemies = []
        self.populate(difficulty)
        self.alive = 1

    def populate(self, diff):
        if diff == 'easy':
            slimes = random.randint(1,3)
            orcs = random.randint(0,1)
            for i in range(slimes):
                mon = Monster("slime")
                self.enemies.append(mon)
            if orcs == 1:
                mon = Monster("orc")
                self.enemies.append(mon)

        elif diff == 'medium':
            slimes = random.randint(0,2)
            orcs = random.randint(1,3)
            if slimes > 0:
                for i in range(slimes):
                    mon = Monster("slime")
                    self.enemies.append(mon)
            for i in range(orcs):
                mon = Monster("orc")
                self.enemies.append(mon)
        else: #diff = hard
            slimes = random.randint(0,2)
            orcs = random.randint(0,2)
            if slimes > 0:
                for i in range(slimes):
                    mon = Monster("slime")
                    self.enemies.append(mon)
            if orcs > 0:
                for i in range(slimes):
                    mon = Monster("orc")
                    self.enemies.append(mon)
            mon = Monster("demon")
            self.enemies.append(mon)

    def showEnemies(self): #TODO destroy all enemies and read
        if(self.alive):
            app.remove_all_enemies()
            stringEncounter = ""
            for i, enemy in enumerate(self.enemies):
                app.loadEnemy(enemy.image, enemy.hp)
                if enemy.name == "orc":
                    stringEncounter += ("There is an " + enemy.name + " with " + str(enemy.hp) + " health.\n")
                else:
                    stringEncounter += ("There is a " + enemy.name + " with " + str(enemy.hp) + " health.\n")
            return stringEncounter
        else:
            return "The remains of enemies are here."

    def act(self,knight): #TODO update health (both knight and enemies, if we are showing enemy health)
        say(self.showEnemies())
        while(self.alive):     
            command = speech_input("Enemies! 'fight' or 'run'? (You have " + str(knight.hp) + " health left.):")
            if "fight" in command:
                rb_container.add_slash_commands()
                for enemy in self.enemies:
                    knight.hp -= enemy.attack()
                    if knight.hp <= 0:
                        say(monsterLoseText)
                        playAgain()
                dmg = knight.attack(self.enemies[0].name)
                self.enemies[0].hp -= dmg
                if self.enemies[0].hp <= 0:
                    say("You killed the " + self.enemies[0].name + "!")
                    self.enemies.pop(0)
                if not self.enemies:
                    say("You defeated the enemies! You have " + str(knight.hp) + " health left.")
                    self.alive = False
                    return True
                else:
                    for enemy in self.enemies:
                        say("The " + enemy.name + " has " + str(enemy.hp) + " health left.")
            elif "run" in command:
                say("You flee, running blindly.")
                return False
            else:
                say("That is not a possible action, try again.")

        return True
            
            

class Monster():
    def __init__(self,name):
        self.name = name
        self.hp = None
        self.dmg = None
        self.typify()
        self.image = "guiPics/"+self.name+".gif"

    def typify(self):
        if self.name=="slime":
            self.hp = random.randint(1,3)
            self.dmg = [i for i in range(0,3)]
        elif self.name=="orc":
            self.hp = random.randint(2,9)
            self.dmg = [i for i in range(0,5)]
        elif self.name=="demon":
            self.hp = random.randint(10,25)
            self.dmg = [2*i for i in range(0,5)]
            
    def attack(self):
        dmg = self.dmg[random.randint(0,len(self.dmg)-1)]
        if dmg==0:
            say("The " + self.name + " misses!")
        else:
            say("The " + self.name + " hits for " + str(dmg) + " damage!")
        return dmg
    

class GameMap():

    ROOM_CONTENT_MAPPING = {"Hint": 'guiPics/runes.jpeg', "Encounter": 'guiPics/dungeon_one.jpeg', "Finish": 'guiPics/throne_room.jpeg', "Start": "guiPics/dungeon_three.jpeg"}

    def __init__(self, adventureMap,knight,easy, queue:Queue, robot_container: RobotContainer):
        self.knight = knight
        self.adventureMap = adventureMap
        self.curRoom = None
        self.endRoom = None
        self.roomContents=[None]*25
        self.populateMap(easy)
        self.facing_dir = "north"
        self.turn_time = 1
        self.drive_time = .5
        self.queue = queue
        self.robot_container = robot_container
        self.speed = .7

    def turnAndMove(self, dir):
        if self.facing_dir == "north":
            if dir == "north":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "east":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.turn_time, self.speed, -self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "south":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, 2*self.turn_time, self.speed, -self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "west":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.turn_time, -self.speed, self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
        elif self.facing_dir == "east":
            if dir == "north":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.turn_time, -self.speed, self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "east":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "south":
                self.queue.put(
                    DriveCommand(self.robot_container.drivetrain, self.turn_time, self.speed, -self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "west":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, 2*self.turn_time, self.speed, -self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
        elif self.facing_dir == "south":
            if dir == "north":
                self.queue.put(
                    DriveCommand(self.robot_container.drivetrain, 2 * self.turn_time, -self.speed, self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "east":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.turn_time, -self.speed, self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "south":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "west":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.turn_time, self.speed, -self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
        elif self.facing_dir == "west":
            if dir == "north":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.turn_time, self.speed, -self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "east":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, 2*self.turn_time, -self.speed, self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "south":
                self.queue.put(
                    DriveCommand(self.robot_container.drivetrain, self.turn_time, -self.speed, self.speed))
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return
            elif dir == "west":
                self.queue.put(DriveCommand(self.robot_container.drivetrain, self.drive_time, self.speed, self.speed))
                return

    def getRelativeDir(self, facing, direction):
        if facing == "north":
            if direction == "north":
                return "forward"
            elif direction == "east":
                return "right"
            elif direction == "south":
                return "back"
            elif direction == "west":
                return "left"
        elif facing == "east":
            if direction == "north":
                return "left"
            elif direction == "east":
                return "forward"
            elif direction == "south":
                return "right"
            elif direction == "west":
                return "back"
        elif facing == "south":
            if direction == "north":
                return "back"
            elif direction == "east":
                return "left"
            elif direction == "south":
                return "forward"
            elif direction == "west":
                return "right"
        elif facing == "west":
            if direction == "north":
                return "right"
            elif direction == "east":
                return "back"
            elif direction == "south":
                return "left"
            elif direction == "west":
                return "forward"

    def getCompassDir(self, facing, direction):
        if facing == "north":
            if direction == "forward":
                return "north"
            elif direction == "right":
                return "east"
            elif direction == "back":
                return "south"
            elif direction == "left":
                return "west"
        elif facing == "east":
            if direction == "left":
                return "north"
            elif direction == "forward":
                return "east"
            elif direction == "right":
                return "south"
            elif direction == "back":
                return "west"
        elif facing == "south":
            if direction == "back":
                return "north"
            elif direction == "left":
                return "east"
            elif direction == "forward":
                return "south"
            elif direction == "right":
                return "west"
        elif facing == "west":
            if direction == "right":
                return "north"
            elif direction == "back":
                return "east"
            elif direction == "left":
                return "south"
            elif direction == "forward":
                return "west"

    def getDir(self):
        turnInc = 1
        dirStr = "Enter Direction (you can go "
        if self.check_key_exist(self.adventureMap[self.curRoom-1],'north'):
            dirStr+= self.getRelativeDir(self.facing_dir, "north") + ' '
        if self.check_key_exist(self.adventureMap[self.curRoom-1],'south'):
            dirStr+= self.getRelativeDir(self.facing_dir, "south") + ' '
        if self.check_key_exist(self.adventureMap[self.curRoom-1],'east'):
            dirStr+= self.getRelativeDir(self.facing_dir, "east") + ' '
        if self.check_key_exist(self.adventureMap[self.curRoom-1],'west'):
            dirStr+= self.getRelativeDir(self.facing_dir, "west") + ' '
        dirStr+='):'
        direction = speech_input(dirStr)
        if direction == 'potion':
            rb_container.add_drink_commands()
            turnInc = 0
            if self.knight.potion == 0:
                say("You don't have any potions")
            else:

                effect = random.randint(1,6)
                if effect == 1:
                    dmg = random.randint(1,10)
                    say("The potion is actually poison! It deals " + str(dmg) + " damage.")
                    self.knight.hp -= dmg
                    say("You have " + str(self.knight.hp) + " health left.")
                    if self.knight.hp <= 0:
                        say("The poison causes you to collapse. YOU LOSE")
                        playAgain()
                else:
                    say("The potion restores your health to full!")
                    self.knight.hp = 100
                    app.healthBar(100)
                self.knight.potion -= 1
                # if potion == 0: TODO
                # destroy potion image
        elif self.check_key_exist(self.adventureMap[self.curRoom-1], self.getCompassDir(self.facing_dir, direction)):
            #say("Going to room: " + str(adventureMap[self.curRoom-1][direction]))
            self.curRoom = adventureMap[self.curRoom-1][direction]
            #TODO change room background
            image_file = self.ROOM_CONTENT_MAPPING[str(self.roomContents[self.curRoom - 1].content)]
            app.loadImage(image_file)

            cardinal_dir = self.getCompassDir(self.facing_dir, direction)

            self.turnAndMove(cardinal_dir)
            self.facing_dir = cardinal_dir

            print("")
            say(self.roomContents[self.curRoom-1].desc)
            if str(self.roomContents[self.curRoom-1].content) == "Hint":
               self.roomContents[self.curRoom-1].content.act(self.knight, self.curRoom, self.endRoom)
            elif str(self.roomContents[self.curRoom-1].content) == "Encounter":
                success = self.roomContents[self.curRoom-1].content.act(self.knight)

                if success: # killed all monsters
                    #TODO monsters dead
                    pass
                else: # runs away
                    self.curRoom = random.randint(1,25)
                    #TODO update room
                    image_file = self.ROOM_CONTENT_MAPPING[str(self.roomContents[self.curRoom - 1].content)]
                    app.loadImage(image_file)
                    self.queue.put(DriveCommand(self.robot_container.drivetrain, 3*self.turn_time, self.speed, -self.speed))
                    say(self.roomContents[self.curRoom-1].desc)
            elif str(self.roomContents[self.curRoom-1].content) == "Finish":
               return (self.roomContents[self.curRoom-1].content.act(self.knight), turnInc)
            else:
                self.roomContents[self.curRoom-1].content.act(self.knight)
        else:
            say("Can't Go that way")
            turnInc = 0

        return (False, turnInc)

    def check_key_exist(self,test_dict, key):
        try:
           value = test_dict[key]
           return True
        except KeyError:
            return False

    def removeAdjacentRooms(self,room,rooms):
        removedRooms = []
        try:
           rooms.remove(room-5)
           removedRooms.append(room-5)
        except ValueError:
            pass
        
        try:
           rooms.remove(room+5)
           removedRooms.append(room+5)
        except ValueError:
            pass

        try:
           rooms.remove(room-1)
           removedRooms.append(room-1)
        except ValueError:
            pass

        try:
           rooms.remove(room+1)
           removedRooms.append(room+1)
        except ValueError:
            pass
            
        return removedRooms

    def start(self):
        say(startDesc)

    def populateMap(self,easy):
        rooms = [i+1 for i in range(25)]
        #say(rooms)

        #create start on an edge
        possibleStartPos = [1,2,3,4,5,10,15,20,25,24,23,22,21,16,11,6]
        self.curRoom = possibleStartPos[random.randint(0,len(possibleStartPos)-1)]
        self.roomContents[self.curRoom-1] = Node(self.curRoom, Start(), startRoomDesc)
        #TODO start room
        image_file = self.ROOM_CONTENT_MAPPING[str(self.roomContents[self.curRoom - 1].content)]
        app.loadImage(image_file)
        rooms.remove(self.curRoom)
        if easy: say("Start placed at "+str(self.curRoom))
        #say(rooms)

        #create end on opposite edge
        if self.curRoom == 1:
            possibleFinishPos = [21,22,23,24,25,20,15,10,5]
        elif self.curRoom in [2,3,4]:
            possibleFinishPos = [21,22,23,24,25]
        elif self.curRoom == 5:
            possibleFinishPos = [1,6,11,16,21,22,23,24,25]
        elif self.curRoom in [10,15,20]:
            possibleFinishPos = [1,6,11,16,21]
        elif self.curRoom == 25:
            possibleFinishPos = [21,16,11,6,1,2,3,4,5]
        elif self.curRoom in [22,23,24]:
            possibleFinishPos = [1,2,3,4,5]
        elif self.curRoom == 21:
            possibleFinishPos = [1,2,3,4,5,10,15,20,25]
        elif self.curRoom in [6,11,16]:
            possibleFinishPos = [5,10,15,20,25]
        

        self.endRoom = possibleFinishPos[random.randint(0,len(possibleFinishPos)-1)]
        self.roomContents[self.endRoom-1] = Node(self.endRoom, Finish(), endRoomDesc)
        rooms.remove(self.endRoom)
        if easy: say("End placed at "+str(self.endRoom))
        #say(rooms)

        #place 3 Recharge Nodes (can't be next to each other)
        adjacentRooms = []
        for i in range(3):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Recharge())
            rooms.remove(room)
            adjacentRooms.extend(self.removeAdjacentRooms(room,rooms))
            if easy: say("Recharge placed at " + str(room))
        rooms.extend(adjacentRooms)
        #say(rooms)
       
        #place 2 Hint Nodes
        adjacentRooms = []
        for i in range(2):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Hint())
            rooms.remove(room)
            adjacentRooms.extend(self.removeAdjacentRooms(room,rooms))
            if easy: say("Hint placed at " + str(room))
        rooms.extend(adjacentRooms)
        #say(rooms)


        #place puzzle Node
        room = rooms[random.randint(0,len(rooms)-1)]
        self.roomContents[room-1] = Node(room, Key())
        rooms.remove(room)
        if easy: say("Key puzzle placed at " + str(room))
        #say(rooms)


        #place 3 ~Other~ Nodes
        for i in range(3):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Other())
            rooms.remove(room)
            if easy: say("~Other~ room placed at " + str(room))
        #say(rooms)
        
        #place 6 easy battles
        for i in range(6):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Encounter("easy"))
            rooms.remove(room)
            if easy: say("Easy Encounter placed at " + str(room))
        #say(rooms)

        #place 5 medium battles
        for i in range(5):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Encounter("medium"))
            rooms.remove(room)
            if easy: say("Medium Encounter placed at " + str(room))
        #say(rooms)

        #place 3 hard battles
        for i in range(3):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Encounter("hard"))
            rooms.remove(room)
            if easy: say("Hard Encounter placed at " + str(room))
        #say(rooms)

        if easy: say("All rooms placed")


class Game():
    def __init__(self, queue: Queue, robot_container:RobotContainer, easy, application: Window):
        self.turnCount = 0
        self.queue = queue
        self.robot_container = robot_container
        global rb_container
        rb_container = self.robot_container
        global app
        app = application
        self.you = Knight()
        self.map = GameMap(adventureMap,self.you, easy, self.queue, self.robot_container)
        self.win = False;
        app.healthBar(100)



    def play(self):
        self.map.start()
        while(not self.win):
            (self.win,inc) = self.map.getDir()
            self.turnCount += inc
            say(f"Turns remaining: {30 - self.turnCount}")
            if self.turnCount > 30:
                say(timeLoseText)
                playAgain()
                exit
        say(winText)
        playAgain()
        return




###############################################################################################
# Helper Methods
###############################################################################################
def playAgain():
    pa=speech_input("Play Again? [y/n]: ")
    if pa == 'y':
        os.execv(sys.argv[0], sys.argv)
    elif pa == 'n':
        exit
    else:
        say("Not a valid command, quitting")
        exit
    exit


def speech_input(output_string):
    say(output_string)
    command = ListenCommand(rb_container.speech_listener)
    rb_container.command_queue.put(command)
    while command.phrase is None:
        pass
    #print("speech returned: " + command.phrase)
    return command.phrase

def say(output_string):
    print(output_string)
    if rb_container.speaker is not None:
        rb_container.command_queue.put(SayPhraseCommand(rb_container.speaker, output_string))

###############################################################################################
# Main Method
###############################################################################################
if __name__ == "__main__":
    g = Game(easy=False)
    g.play()
