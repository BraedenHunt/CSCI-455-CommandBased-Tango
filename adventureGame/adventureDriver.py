from mapVariable import *
from descriptionText import *
import random
import os
import sys



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
        self.key=False      # do you have the key?
        self.sword=False    # do you have the magic sword
        self.potion=0       # what potion do you have

    def attack(self, target):
        mult = 1
        if self.sword:
            mult = 3
        dmg = mult * random.randint(0,8)
        if dmg==0:
            print("Oh no, you missed!")
        else:
            print("You hit the " + target + " for " + str(dmg) + " damage!")
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
            print("Luckily, you have the key!")
            return True
        else:
            print("Looks like you need a key.")
            return False

class Other():
    def __repr__(cls):
        return 'Other'

    def __init__(self):
        self.type = random.randint(1,5)
        self.used = False
    
    def act(self,knight):
        if(not self.used):
            answer = input("Something is off about this room, investigate? [y/n]: ")
            if answer == 'n':
                return
            else:
                if self.type == 1:
                    print("You find a magical blade, glowing with power! It will help you fight monsters.")
                    knight.sword = True
                elif self.type > 1 and self.type < 5:
                    print("You find a bottle filled with a swirling liquid, a potion! When not fighting, type 'potion' to use.\n But beware, who knows what it does!")
                    knight.potion+=1
                else:
                    dmg = random.randint(5,15)
                    print("You spring a hidden trap! The swinging blade hits you for " + str(dmg) + " damage!")
                    knight.hp -= dmg
                    if knight.hp <= 0:
                        print(trapLoseText)
                        playAgain()
                self.used = True           
        else:
            print("There is nothing else to find here.")

class Recharge():
    def __repr__(cls):
        return 'Recharge'
    
    def __init__(self):
        self.used = False
        
    def act(self,knight):
        if(not self.used):
            if knight.hp == 100:
                print("Magic runes carved here could refill your health, if you were hurt.")
                return
            else:
                knight.hp = 100
                print("The magic runes carved here refill your health")
                self.used = True
        else:
            print("The magic runes here have been used.")

class Key():
    def __repr__(cls):
        return 'Key'

    def __init__(self):
        self.used = False
        self.solution = random.randint(0,1)
    
    def act(self,knight):
        if(not self.used):
            print("A golden chest sits in the center of this room, carved with a square and a triangle.")
            if self.solution:
                print("A riddle reads: The number of musketeers is the key.")
            else:
                print("A riddle reads: The turning of the seasons reveals the key")

            choice = input("What do you choose? [square, triangle, leave]: ")

            if choice == 'square':
                numChoice = 0
            elif choice == 'triangle':
                numChoice = 1
            elif choice == 'leave':
                return
            else:
                print("That is not a valid choice, come back later")
                return

            if numChoice == self.solution:
                print("At the press of the button, the chest opens, revealing a key!")
                knight.key = True
            else:
                    dmg = random.randint(15,50)
                    print("The wrong choice! A poison needle jabs you for " + str(dmg) + " damage!\nPressing the other button, you find a key.")
                    knight.key = True
                    knight.hp -= dmg
                    if knight.hp <= 0:
                        print(trapLoseText)
                        playAgain()
            self.used = True           
        else:
            print("There is nothing else to find here.")

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
        
        print("A cryptic message points the way: the exit is " + hint + " of here.")

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
        self.populate(difficulty)
        self.alive = 1

    def populate(self, diff):
        if diff == 'easy':
            slimes = random.randint(1,3)
            orcs = random.randint(0,1)
            for i in range(slimes):
                self.enemies.append(Monster("slime"))
            if orcs == 1:
                self.enemies.append(Monster("orc"))
                
        elif diff == 'medium':
            slimes = random.randint(0,2)
            orcs = random.randint(1,3)
            if slimes > 0:
                for i in range(slimes):
                    self.enemies.append(Monster("slime"))
            for i in range(orcs):
                self.enemies.append(Monster("orc"))
        else: #diff = hard
            slimes = random.randint(0,2)
            orcs = random.randint(0,2)
            if slimes > 0:
                for i in range(slimes):
                    self.enemies.append(Monster("slime"))
            if orcs > 0:
                for i in range(slimes):
                    self.enemies.append(Monster("orc"))
            self.enemies.append(Monster("demon"))

    def showEnemies(self):
        if(self.alive):
            stringEncounter = ""
            for enemy in self.enemies:
                if enemy.name == "orc":
                    stringEncounter += ("There is an " + enemy.name + " with " + str(enemy.hp) + " health.\n")
                else:
                    stringEncounter += ("There is a " + enemy.name + " with " + str(enemy.hp) + " health.\n")
            return stringEncounter
        else:
            return "The remains of enemies are here."

    def act(self,knight):
        print(self.showEnemies())
        while(self.alive):     
            command = input("Enemies! 'fight' or 'run'? (You have " + str(knight.hp) + " health left.):")
            if command == "fight":
                for enemy in self.enemies:
                    knight.hp -= enemy.attack()
                    if knight.hp <= 0:
                        print(monsterLoseText)
                        playAgain()
                dmg = knight.attack(self.enemies[0].name)
                self.enemies[0].hp -= dmg
                if self.enemies[0].hp <= 0:
                    print("You killed the " + self.enemies[0].name + "!")
                    self.enemies.pop(0)
                if not self.enemies:
                    print("You defeated the enemies! You have " + str(knight.hp) + " health left.")
                    self.alive = False
                    return True
                else:
                    for enemy in self.enemies:
                        print("The " + enemy.name + " has " + str(enemy.hp) + " health left.")
            elif command == 'run':
                print("You flee, running blindly.")
                return False
            else:
                print("That is not a possible action, try again.")

        return True
            
            

class Monster():
    def __init__(self,name):
        self.name = name
        self.hp = None
        self.dmg = None
        self.typify()

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
            print("The " + self.name + " misses!")
        else:
            print("The " + self.name + " hits for " + str(dmg) + " damage!")
        return dmg
    

class GameMap():
    def __init__(self, adventureMap,knight,easy):
        self.knight = knight
        self.adventureMap = adventureMap
        self.curRoom = None
        self.endRoom = None
        self.roomContents=[None]*25
        self.populateMap(easy)

    def getDir(self):
        turnInc = 1
        dirStr = "Enter Direction (you can go "
        if self.check_key_exist(self.adventureMap[self.curRoom-1],'north'):
            dirStr+='north '
        if self.check_key_exist(self.adventureMap[self.curRoom-1],'south'):
            dirStr+='south '
        if self.check_key_exist(self.adventureMap[self.curRoom-1],'east'):
            dirStr+='east '
        if self.check_key_exist(self.adventureMap[self.curRoom-1],'west'):
            dirStr+='west '
        dirStr+='):'
        direction = input(dirStr)
        if direction == 'potion':
            turnInc = 0
            if self.knight.potion == 0:
                print("You don't have any potions")
            else:
                effect = random.randint(1,6)
                if effect == 1:
                    dmg = random.randint(1,10)
                    print("The potion is actually poison! It deals " + str(dmg) + " damage.")
                    self.knight.hp -= dmg
                    print("You have " + self.knight.hp + " health left.")
                    if self.knight.hp <= 0:
                        print("The poison causes you to collapse. YOU LOSE")
                        playAgain()
                else:
                    print("The potion restores your health to full!")
                    self.knight.hp = 100
                self.knight.potion -= 1
        elif self.check_key_exist(self.adventureMap[self.curRoom-1],direction):
            #print("Going to room: " + str(adventureMap[self.curRoom-1][direction]))
            self.curRoom = adventureMap[self.curRoom-1][direction]
            print("")
            print(self.roomContents[self.curRoom-1].desc)
            if str(self.roomContents[self.curRoom-1].content) == "Hint":
               self.roomContents[self.curRoom-1].content.act(self.knight, self.curRoom, self.endRoom)
            elif str(self.roomContents[self.curRoom-1].content) == "Encounter":
                success = self.roomContents[self.curRoom-1].content.act(self.knight)
                if success:
                    pass
                else:
                    self.curRoom = random.randint(1,25)
                    print(self.roomContents[self.curRoom-1].desc)
            elif str(self.roomContents[self.curRoom-1].content) == "Finish":
               return (self.roomContents[self.curRoom-1].content.act(self.knight), turnInc)
            else:
                self.roomContents[self.curRoom-1].content.act(self.knight)
        else:
            print("Can't Go that way")
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
        print(startDesc)

    def populateMap(self,easy):
        rooms = [i+1 for i in range(25)]
        #print(rooms)

        #create start on an edge
        possibleStartPos = [1,2,3,4,5,10,15,20,25,24,23,22,21,16,11,6]
        self.curRoom = possibleStartPos[random.randint(0,len(possibleStartPos)-1)]
        self.roomContents[self.curRoom-1] = Node(self.curRoom, Start(), startRoomDesc)
        rooms.remove(self.curRoom)
        if easy: print("Start placed at "+str(self.curRoom))
        #print(rooms)

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
        if easy: print("End placed at "+str(self.endRoom))
        #print(rooms)

        #place 3 Recharge Nodes (can't be next to each other)
        adjacentRooms = []
        for i in range(3):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Recharge())
            rooms.remove(room)
            adjacentRooms.extend(self.removeAdjacentRooms(room,rooms))
            if easy: print("Recharge placed at " + str(room))
        rooms.extend(adjacentRooms)
        #print(rooms)
       
        #place 2 Hint Nodes
        adjacentRooms = []
        for i in range(2):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Hint())
            rooms.remove(room)
            adjacentRooms.extend(self.removeAdjacentRooms(room,rooms))
            if easy: print("Hint placed at " + str(room))
        rooms.extend(adjacentRooms)
        #print(rooms)


        #place puzzle Node
        room = rooms[random.randint(0,len(rooms)-1)]
        self.roomContents[room-1] = Node(room, Key())
        rooms.remove(room)
        if easy: print("Key puzzle placed at " + str(room))
        #print(rooms)


        #place 3 ~Other~ Nodes
        for i in range(3):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Other())
            rooms.remove(room)
            if easy: print("~Other~ room placed at " + str(room))
        #print(rooms)
        
        #place 6 easy battles
        for i in range(6):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Encounter("easy"))
            rooms.remove(room)
            if easy: print("Easy Encounter placed at " + str(room))
        #print(rooms)

        #place 5 medium battles
        for i in range(5):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Encounter("medium"))
            rooms.remove(room)
            if easy: print("Medium Encounter placed at " + str(room))
        #print(rooms)

        #place 3 hard battles
        for i in range(3):
            room = rooms[random.randint(0,len(rooms)-1)]
            self.roomContents[room-1] = Node(room, Encounter("hard"))
            rooms.remove(room)
            if easy: print("Hard Encounter placed at " + str(room))
        #print(rooms)

        if easy: print("All rooms placed")


class Game():
    def __init__(self, easy):
        self.turnCount = 0
        self.you = Knight()
        self.map = GameMap(adventureMap,self.you,easy)
        self.win = False;


    def play(self):
        self.map.start()
        while(not self.win):
            (self.win,inc) = self.map.getDir()
            self.turnCount += inc
            print(f"Turns remaining: {30 - self.turnCount}")
            if self.turnCount > 30:
                print(timeLoseText)
                playAgain()
                exit
        print(winText)
        playAgain()
        return




###############################################################################################
# Helper Methods
###############################################################################################
def playAgain():
    pa=input("Play Again? [y/n]: ")
    if pa == 'y':
        os.execv(sys.argv[0], sys.argv)
    elif pa == 'n':
        exit
    else:
        print("Not a valid command, quitting")
        exit
    exit



    
###############################################################################################
# Main Method
###############################################################################################
if __name__ == "__main__":
    g = Game(easy=False)
    g.play()
