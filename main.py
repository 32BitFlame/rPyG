plr = None;
gameActive = True;
import random as r
import os
import json
import readchar
Globals = json.loads(str(open("globals.json", "r").read()))
print(Globals)
read = readchar.readchar()
Debug = True;
currentDirectory = os.path.dirname(__file__)
options_GUI = bool(open(os.path.join(currentDirectory, "options/options_gui"), "r").read())
Rooms = {}
gameOver = False;

def clearShell():
  try:
    os.system("cls")
  except:
    os.system("clear")

def clampDown(variable, minimum):
  return max(variable, minimum)

def clampUp(variable, maximum):
  return min(variable, maximum)

def randomDecimal(floatA, floatB):
  return (round((r.randrange(floatA * 10, floatB * 10))*0.1))

class BattleAction():
  def __init__(self, parent, energyUsage, useEnergyOnAttack):
    self.Parent = parent
    self.energyUsage = energyUsage * int(useEnergyOnAttack)
  def BattleAction():
    pass

class BattleAction_Attack(BattleAction):
  def __init__(self, parent, actionText, effect, energyUsage, useEnergyOnAttack):
    self.ActionText = actionText;
    self.Effect = effect
    BattleAction.__init__(self, parent, energyUsage, useEnergyOnAttack)
  def do(self, targetCharacter):    
    print(self.parent.Name + self.actionText + targetCharacter.Name)
    try:
      targetCharacter.health -= self.Effect
    except:
      raise "targetCharacter is not infact a charcater"

class Battle():
  def __init__(self, enemies):
    self.enemies = enemies;
  def start(self):
    global gameOver
    global plr
    clearShell()
    while True:
      print("Player:")
      print(plr)
      print("\n Enemies:")
      for ent in self.enemies:
        print(ent)
      plr.BattleAction()
      for entIndex in range(len(self.enemies)):
        if(self.enemies[entIndex].health <= 0):
          print(str(self.enemies[entIndex].Name) + " is down")
      ent.BattleAction()
      if(plr.health <= 0):
        gameOver = True;
        break

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
  def __init__(self, health, baseAttack, baseDefense, modifier, name, actions=[]):
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
  def __init__(self, Name, battleActions):
    NPC.__init__(self, 25 * randomDecimal(0.5, 1.5), 5 * randomDecimal(0.5, 1.5), 3 * randomDecimal(0.5, 1.5), 1, Name)
    self.inventory = []
    self.x, self.y = 0,0;
    self.Actions = battleActions
  def __str__(self):
    return("{0}: Health: {1}, Attack: {2}, Defence {3} \n".format(self.name, self.health, self.atk, self.defence))
  def BattleAction(self, targets):
    choice = 0
    target = 0;
    while True:
      try:
        choice = int(input("Choice: "))
        if((choice >= len(self.Actions) or (choice < 0))):
          raise
      except:
        print("Please enter a valid number")
        continue
      break
    target = 0;
    while True:
      try:
        target = int(input("Choice: "))
        if((target >= len(targets) or (target < 0))):
          raise
      except:
        print("Please enter a valid number")
        continue
      break
    self.Actions[choice].do(target)

class action():
  def do(self):
    pass

#Items
class item():
  def __init__(self, name):
    self.name = name
  def use(self, target):
    print("use")
    del(self)
  def __str__(self):
    return(self.name)

class healingItem(item):
  def __init__(self, Amount, name):
    self.amount = Amount
    self.name = name
  def use(self, target):
    target.health += self.amount;
    del(self)

class exitapp(action):
  def __init__(self):
      pass
  def do(self):
    global gameActive;
    gameActive = False;
exitHandler = exitapp();

class inventoryHandler(action):
  def do(self):
    while True:
      global plr
      localInventory = plr.inventory[:]
      for itemIndex in range(len(localInventory)):
        print("{0}. {1}".format(itemIndex, localInventory[itemIndex]))
      print("{0}. {1}".format(len(localInventory), "Exit Inventory"))
      indexTarget = 0
      while True:
        try:
          indexTarget = int(input())
        except:
          print("Please enter a number")
          continue;
        break
      if(indexTarget == len(localInventory)):
        break
      plr.inventory[indexTarget].use(plr);
      del(plr.inventory[indexTarget]) 
invHandler = inventoryHandler()  

#Room one individual area
class room():
  def __init__(self, x, y, intro, room_actions={}):
    self.started = False;
    global exitHandler
    self.actions = room_actions
    self.actions["quit"] = exitHandler
    global invHandler
    self.actions["Inventory"] = invHandler
    world.SET(x,y,self)
    self.introFin = False;
    self.intro = intro
  def action(self):
    global plr
    global gameOver
    if(not(self.started)):
      try:
        self.actions["init"].do();
      except:
        pass
      self.started = True;
    print(self.intro)
    room_actions_list = list(self.actions.keys())
    while True:
      try:
        self.actions[input(room_actions_list)].do()
      except KeyError:
        print("Command does not exist")
        continue
      break
    if(plr.health <= 0):
      gameOver = True;
    

#Any actions that heal a character
class roomAction_heal():
  def do(self, objectInRoomStr, target, effect, desc):
    print("{0}{1}{2}".format(objectInRoomStr, desc, target))
    target.health += effect
    del(self)

#Any actions that do damage to a character
class roomAction_attack():
  def __init__(self,attacker, attackOn, effect, desc):
    self.owner=attacker
    self.attackOn=attackOn
    self.effect=1 
    self.desc=" did a thing to "
  def do(self):
    print("{0}{1}{2}".format(self.owner, self.desc, self.attackOn.name))
    self.attackOn.health -= self.effect
    del(self)

class enemy():
  def __init__(self, health, damage, defence, Name, actions):
    NPC.__init__(self, health, damage, defence, name=Name)
    self.Actions = actions
    self.actionprob = []
  def BattleAction(self):
    global plr
    choice = r.randint(0, len(self.actionprob)-1)
    if(len(self.actionprob) == 0):
      print(self.name + "couldn't do anything")
      return
    self.actionsprob[choice].do(plr)

class roomAction_changeRoom():
  def __init__(self, x, y):
    self.newX = x
    self.newY = y
  def do(self):
    global plr
    global world
    plr.x = self.newX
    plr.y = self.newY

class roomAction_dealDamage():
  def __init__(self, damage, text):
    self.Damage = damage
    self.Text = text
  def do(self):
    print(self.Text)
    plr.health-=self.Damage

class roomAction_itemGet():
  def __init__(self, text="got a thing", item=healingItem(10, "Potion")):
    self.Item = item;
  def do(self):
    global plr
    plr.inventory.append(self.Item)
    
class roomAction_displayText():
  def __init__(self, text):
    self.text= text;
  def do(self):
    print(self.text)

class jsonActionHandler_par():  
  def do(self, actionHandler):
    raise "not implemented"

class jsonActionHandler_InitBattle():
  def __init__(self, actionDictionary):
    npcsDicts = actionDictionary["npcs"]
    for npc in npcsDicts:
      newChar = enemy(npc["health"], npc["damage"], defence, Name, actions)

class jsonActionHandler_typeof_changeroom(jsonActionHandler_par):
  def do(self, actionDictionary):
    target_x = int(actionDictionary["target_x"])
    target_y = int(actionDictionary["target_y"])
    return roomAction_changeRoom(target_x, target_y)

class jsonActionHandler_typeof_dealDamage():
  def do(self, actionDictionary):
    return roomAction_dealDamage(actionDictionary["damage"], actionDictionary["text"])

class jsonActionHandler_typeof_displayText():
  def do(self, actionDictionary):
    return(roomAction_displayText(actionDictionary["text"]))

class jsonActionHandler_typeof_itemGet_heal(jsonActionHandler_par):
  def do(self, actionDictionary):
    itemDictionary = actionDictionary["item"]
    return(roomAction_itemGet(item=healingItem(itemDictionary["amount"], itemDictionary["name"])))

jsonActionHandlers={
  "changeRoom":jsonActionHandler_typeof_changeroom(),
  "giveItem_heal":jsonActionHandler_typeof_itemGet_heal(),
  "displayText":jsonActionHandler_typeof_displayText(),
  "dealDamage":jsonActionHandler_typeof_dealDamage()
}

class jsonActionHandler_typeof_itemGet(jsonActionHandler_par):
  def do(self, actionDictionary):
    itemDictionary = actionDictionary["item"]
    return(jsonActionHandlers[itemDictionary["type"]].do(actionDictionary))

os.chdir(os.path.join(currentDirectory, "rooms"))

for roomFile in os.listdir():
  print(roomFile)
  currentRoomFile = open(roomFile, "r").read()
  roomData = json.loads(currentRoomFile)
  actionsDictionary = json.loads(roomData["Actions"])
  roomActions = {}
  for actionKey in actionsDictionary.keys():
    currentDictionary = actionsDictionary[actionKey];
    roomActions[actionKey]=jsonActionHandlers[currentDictionary["type"]].do(currentDictionary)
  room(int(roomData["x"]), int(roomData["y"]), roomData["intro"], room_actions=roomActions)
  
os.chdir("..")
#Game Test
try:
  print("Shell required \n")
  plr = player(str(input("Player Name: ")), [])  
  while not(gameOver):
    print(plr)
    world.GET(int(plr.x), int(plr.y)).action()
    input("Press enter to continue")
except:
  open("errorDump.txt", "w").close()
  dumpFile = open("errorDump.txt", "a")
  for x in globals():
    dumpFile.write(str(id(x))+str(x) +"\n")
  for x in locals():
    dumpFile.write(str(id(x))+str(x)+"\n")
