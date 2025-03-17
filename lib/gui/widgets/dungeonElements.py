from lib.gui.widgets.labelBox import LabelBox
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from lib.util.enums import INVENTORY
import tkinter as tk

class DungeonItem:
  name  = "UNK"
  level = -1
  found_smalls = -1


  def __init__(self, canvas:tk.Canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    self.canvas = canvas
    self.zelda = zelda
    self.background = canvas.create_rectangle(x, y, x+width, y+height, fill="#DDDDDD")
    self.x = x
    self.width = width
    self.y = y
    self.height = height
    yOff = 5
    xOff = 5
    self.levelText = self.canvas.create_text(x+xOff, y+yOff, text=f"Level {self.level} - {self.name}", anchor=tk.NW)
    yOff += 15
    self.keysText  = self.canvas.create_text(x+xOff, y+yOff, text=f"Small Keys: {self.found_smalls}", anchor=tk.NW)
    yOff += 15

    boxWidth = width-10

    self.dungeonMarkers = {
      "complete": LabelBox(self.canvas, x+xOff,               y+yOff,    boxWidth,    15, "Complete",     "pink"),
      "miniboss": LabelBox(self.canvas, x+xOff,               y+yOff+15, boxWidth//2, 15, "Mini-Boss",    "pink"),
      "boss":     LabelBox(self.canvas, x+xOff+boxWidth-boxWidth//2,   y+yOff+15, boxWidth//2, 15, "Nightmare",    "pink"),
      "item":     LabelBox(self.canvas, x+xOff,               y+yOff+30, boxWidth//2, 15, "Item", "pink"),
      "bigKey":   LabelBox(self.canvas, x+xOff+boxWidth-boxWidth//2,   y+yOff+30, boxWidth//2, 15, "Big Key",      "pink"),
      "map":      LabelBox(self.canvas, x+xOff,               y+yOff+45, boxWidth//2, 15, "Map",          "pink"),
      "compass":  LabelBox(self.canvas, x+xOff+boxWidth-boxWidth//2,   y+yOff+45, boxWidth//2, 15, "Compass",      "pink"),
      "beak":     LabelBox(self.canvas, x+xOff,               y+yOff+60, boxWidth//2, 15, "Beak",         "pink"),
      "key":      LabelBox(self.canvas, x+xOff+boxWidth-boxWidth//2,   y+yOff+60, boxWidth//2, 15, "Main Key",     "pink")
    }

    self.dungeonSpecifics = []

  def update(self):
    if self.level-1 not in range(8):
      return
    dungeonItems = self.zelda.getDungeonItems()[self.level-1]
    # bossFlags is hHasInstrumentN and is 1 if miniboss is defeated, or 2 if instrument is obtained
    bossFlags = self.zelda.getBossFlags()[self.level-1]

    # bossStatus checks the wIndoorXRoomStatus for the 0x20 flag, it's true if the boss is defeated
    bossStatus = self.zelda.getBossStatus()[self.level-1]
    self.canvas.itemconfig(self.keysText, text=f"Small Keys: {dungeonItems.smallKeys}")
    
    if dungeonItems.map:
      self.dungeonMarkers['map'].updateFill("lightgreen")
    else:
      self.dungeonMarkers['map'].updateFill("pink")
    
    if dungeonItems.compass:
      self.dungeonMarkers['compass'].updateFill("lightgreen")
    else:
      self.dungeonMarkers['compass'].updateFill("pink")
    
    if dungeonItems.beak:
      self.dungeonMarkers['beak'].updateFill("lightgreen")
    else:
      self.dungeonMarkers['beak'].updateFill("pink")
    
    if dungeonItems.bossKey:
      self.dungeonMarkers['bigKey'].updateFill("lightgreen")
    else:
      self.dungeonMarkers['bigKey'].updateFill("pink")

    self.dungeonMarkers['complete'].updateFill("pink")
    self.dungeonMarkers['boss'].updateFill("pink")
    self.dungeonMarkers['miniboss'].updateFill("pink")

    if bossFlags & 1: # Miniboss is defeated
      self.dungeonMarkers['miniboss'].updateFill("lightgreen")

    if bossStatus: # Boss is defeated
      self.dungeonMarkers['miniboss'].updateFill("lightgreen")
      self.dungeonMarkers['boss'].updateFill("lightgreen")

    if bossFlags & 2: # Dungeon is totally complete
      self.dungeonMarkers['complete'].updateFill("lightgreen")
      self.dungeonMarkers['boss'].updateFill("lightgreen")
      self.dungeonMarkers['miniboss'].updateFill("lightgreen")
    
    if self.isOpen():
      self.dungeonMarkers['key'].updateFill("lightgreen")
    else:
      self.dungeonMarkers['key'].updateFill("pink")
    
    if self.hasItem():
      self.dungeonMarkers['item'].updateFill("lightgreen")
    else:
      self.dungeonMarkers['item'].updateFill("pink")
    

    
  def isOpen(self):
    return False
    
  def hasItem(self):
    return False

  def reset(self):
    self.updateFill('white')
    self.updateText(self.name)
  
  def __repr__(self):
    if self.box:
      return f"{type(self).__name__} at {self.canvas.coords(self.box)}"
    else:
      return f"{type(self).__name__} at UNDEFINED"


class TailCave(DungeonItem):
  def __init__(self, canvas, zelda, x, y, width, height):
    self.name = "Tail Cave"
    self.level = 1
    super().__init__(canvas, zelda, x, y, width, height)
  
  def isOpen(self):
    return self.zelda.getInventory().tailKey
  
  def hasItem(self):
    return self.zelda.getInventory().roc


class BottleGrotto(DungeonItem):
  def __init__(self, canvas, zelda, x, y, width, height):
    self.name = "Bottle Grotto"
    self.level = 2
    super().__init__(canvas, zelda, x, y, width, height)
  
  def isOpen(self):
    return self.zelda.getFlags().bowWow & 1 or self.zelda.getInventory().boomerang or self.zelda.getInventory().hookshot or self.zelda.getInventory().magicRod
  
  def hasItem(self):
    return self.zelda.getInventory().brace


class KeyCavern(DungeonItem):
  def __init__(self, canvas, zelda, x, y, width, height):
    self.name = "Key Cavern"
    self.level = 3
    super().__init__(canvas, zelda, x, y, width, height)
  
  def isOpen(self):
    return self.zelda.getInventory().slimeKeyOrLeaves >= 6
  
  def hasItem(self):
    return self.zelda.getInventory().boots


class AnglersPond(DungeonItem):
  def __init__(self, canvas, zelda, x, y, width, height):
    self.name = "Angler's Pond"
    self.level = 4
    super().__init__(canvas, zelda, x, y, width, height)
  
  def isOpen(self):
    return self.zelda.getInventory().anglerKey
  
  def hasItem(self):
    return self.zelda.getInventory().flippers


class CatfishMaw(DungeonItem):
  def __init__(self, canvas, zelda, x, y, width, height):
    self.name = "Catfish's Maw"
    self.level = 5
    super().__init__(canvas, zelda, x, y, width, height)
  
  def isOpen(self):
    return self.zelda.getInventory().flippers
  
  def hasItem(self):
    return self.zelda.getInventory().hookshot


class FaceShrine(DungeonItem):
  def __init__(self, canvas, zelda, x, y, width, height):
    self.name = "Face Shrine"
    self.level = 6
    super().__init__(canvas, zelda, x, y, width, height)
  
  def isOpen(self):
    return self.zelda.getInventory().faceKey
  
  def hasItem(self):
    return self.zelda.getInventory().brace >= 2


class EaglesTower(DungeonItem):
  def __init__(self, canvas, zelda, x, y, width, height):
    self.name = "Eagles Tower"
    self.level = 7
    super().__init__(canvas, zelda, x, y, width, height)
  
  def isOpen(self):
    return self.zelda.getInventory().birdKey
  
  def hasItem(self):
    return self.zelda.getInventory().shield >= 2


class TurtleRock(DungeonItem):
  def __init__(self, canvas, zelda, x, y, width, height):
    self.name = "Turtle Rock"
    self.level = 8
    super().__init__(canvas, zelda, x, y, width, height)
  
  def isOpen(self):
    return self.zelda.getInventory().shield >= 2
  
  def hasItem(self):
    return self.zelda.getInventory().magicRod
