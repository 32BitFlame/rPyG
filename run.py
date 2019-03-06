#I am bored.jpg
#A game by me
#Copyright non-existant, please don't steal

#/---------------------\#
#|  - INITALIZATION -  |#
#\---------------------/#\
plr = None;
gameActive = True;
import random as r
import os
currentDirectory = os.path.dirname(__file__)
options_GUI = bool(open(os.path.join(currentDirectory, "options/options_gui"), "r").read())
print(options_GUI)
def randomDecimal(floatA, floatB):
  return ((r.randrange(floatA * 10, floatB * 10))*0.1)
class MAP():
  def __init__(self):
    self.raw = []
    for x in range(0,4):
      point = None
      point = []
      for y in range(0,4):
        point.append(None)
      self.raw.append(point)
  def __str__(self):
    print(self.raw)
  def SET(self, x, y, data):
    self.raw[x][y] = data
  def GET_COL(self, x):
    contents = [self.raw[x][0],self.raw[x][1],self.raw[x][2],self.raw[x][3]]
    return contents
  def GET_ROW(self, y):
    contents = [self.raw[0][y],self.raw[1][0],self.raw[2][0],self.raw[3][0]]
    return contents
  def GET(self, x, y):
    return self.raw[x][y]
world = MAP()
class NPC():
  def __init__(self, health, baseAttack, baseDefense, modifier=1, name="NPC", actions=[]):
    self.name = name
    self.health = health * modifier
    self.maxHealth = health
    self.atk = baseAttack * modifier
    self.defence = baseDefense * modifier
    self.actions = actions
  def __str__(self):
    with self as s:
      return("{0}: Health: {1}, Attack: {2}, Defence {3}".format(s.name, s.health, s.atk, s.defence))
  def getStats(self):
    with self:
      return((name, health, atk, defence))
class player():
  def __init__(self, Name):
    NPC.__init__(self, 25 * randomDecimal(0.5, 1.5), 5 * randomDecimal(0.5, 1.5), 3 * randomDecimal(0.5, 1.5), name=Name)
    self.inventory = []
    self.x, self.y = 0,0;
  def __str__(self):
    return("{0}: Health: {1}, Attack: {2}, Defence {3}".format(self.name, self.health, self.atk, self.defence))
if(not(options_GUI)):
  print("Your name please?")
  plr = player(input("Name: "))
  print(plr)
#Items
class healingItem():
  def __init__(self, Amount=1, name="generic"):
    self.amount = Amount
    self.name = name
  def use(self, player, playerUsed):
    player.health += self.amount;
    print()
class exitapp():
  def __init__(self):
      pass
  def do(self):
    global gameActive;
    gameActive = False;
#Room one individual area
class room():
  def __init__(self, room_actions, x, y, intro="none"):
    self.actions = room_actions
    self.actions["quit"] = exitapp()
    world.SET(x,y,self)
    self.introFin = False;
    self.intro = intro
  def action(self):
    print(self.intro)
    room_actions_list = list(self.actions.keys())
    try:
      self.actions[input(room_actions_list)].do()
    except IOError:
      print("Your data may be corrupt")
    except KeyError:
      print("Command does not exist")

#Any actions that heal a character
class roomAction_heal():
  def do(self, owner=None, heal=None, effect=1, desc=" did a thing to "):
    print("{0}{1}{2}".format(owner, desc, heal))
    heal.health += effect
    del(self)

#Any actions that do damage to a character
class roomAction_attack():
  def __init__(self,attacker=NPC(10,10,10,name="dummy"), attackOn=NPC(10,10,10,name="dummy"), effect=1, desc=" did a thing to "):
    self.owner=attacker
    self.attackOn=attackOn
    self.effect=1 
    self.desc=" did a thing to "
  def do(self):
    print("{0}{1}{2}".format(self.owner, self.desc, self.attackOn.name))
    self.attackOn.health -= self.effect
    del(self)
class enemy():
  def __init__(self, health, damage, defence, Name):
    NPC.__init__(self, health, damage, defence, name=Name)
class roomAction_changeRoom():
  def __init__(self, x, y):
    self.newX = x
    self.newY = y
  def do(self):
    global plr
    plr.x = self.newX
    plr.y = self.newY

class roomAction_itemGet():
  def __init__(self, text="got a thing", item=healingItem()):
    global plr
    plr.inventory.append(item)
os.chdir(os.path.join(currentDirectory, "rooms"))
allRoomsDir = {}
for roomFile in os.listdir():
  allRoomsDir[roomFile] = "rooms/"+roomFile
  print(roomFile)
if(options_GUI):
  print("GUI mode")
else:
  print("Shell mode")
