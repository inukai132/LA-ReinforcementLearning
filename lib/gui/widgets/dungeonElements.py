from lib.gui.widgets.labelBox import LabelBox
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from lib.util.utils import getDungeonItems, getOpenDungeons
from lib.gui.widgets.mycanvas import MyCanvas
import tkinter as tk

class DungeonItem:
  name  = "UNK"
  level = 0
  found_smalls = -1


  def __init__(self, canvas:MyCanvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    self.canvas = canvas
    self.zelda = zelda
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.background = self.canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill="#DDDDDD")
    yOff = 5
    xOff = 5
    self.levelText = self.canvas.draw_text(self.x+xOff, self.y+yOff, f"Level {self.level} - {self.name}")
    yOff += 15
    self.keysText  = self.canvas.draw_text(self.x+xOff, self.y+yOff, f"Small Keys: {self.found_smalls}")
    yOff += 15

    boxWidth = width-10

    self.dungeonMarkers = {
      "complete": LabelBox(self.canvas, self.x+xOff,                      self.y+yOff,    boxWidth,    15, "Complete",  "#F08080", fontSize=8),
      "miniboss": LabelBox(self.canvas, self.x+xOff,                      self.y+yOff+15, boxWidth//2, 15, "Mini-Boss", "#F08080", fontSize=8),
      "boss":     LabelBox(self.canvas, self.x+xOff+boxWidth-boxWidth//2, self.y+yOff+15, boxWidth//2, 15, "Nightmare", "#F08080", fontSize=8),
      "item":     LabelBox(self.canvas, self.x+xOff,                      self.y+yOff+30, boxWidth//2, 15, "Item",      "#F08080", fontSize=8),
      "bigKey":   LabelBox(self.canvas, self.x+xOff+boxWidth-boxWidth//2, self.y+yOff+30, boxWidth//2, 15, "Big Key",   "#F08080", fontSize=8),
      "map":      LabelBox(self.canvas, self.x+xOff,                      self.y+yOff+45, boxWidth//2, 15, "Map",       "#F08080", fontSize=8),
      "compass":  LabelBox(self.canvas, self.x+xOff+boxWidth-boxWidth//2, self.y+yOff+45, boxWidth//2, 15, "Compass",   "#F08080", fontSize=8),
      "beak":     LabelBox(self.canvas, self.x+xOff,                      self.y+yOff+60, boxWidth//2, 15, "Beak",      "#F08080", fontSize=8),
      "key":      LabelBox(self.canvas, self.x+xOff+boxWidth-boxWidth//2, self.y+yOff+60, boxWidth//2, 15, "Main Key",  "#F08080", fontSize=8)
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
      self.dungeonMarkers['map'].update(fill="#ADD8E6")
    else:
      self.dungeonMarkers['map'].update(fill="#F08080")
    
    if dungeonItems.compass:
      self.dungeonMarkers['compass'].update(fill="#ADD8E6")
    else:
      self.dungeonMarkers['compass'].update(fill="#F08080")
    
    if dungeonItems.beak:
      self.dungeonMarkers['beak'].update(fill="#ADD8E6")
    else:
      self.dungeonMarkers['beak'].update(fill="#F08080")
    
    if dungeonItems.bossKey:
      self.dungeonMarkers['bigKey'].update(fill="#ADD8E6")
    else:
      self.dungeonMarkers['bigKey'].update(fill="#F08080")

    self.dungeonMarkers['complete'].update(fill="#F08080")
    self.dungeonMarkers['boss'].update(fill="#F08080")
    self.dungeonMarkers['miniboss'].update(fill="#F08080")

    if bossFlags & 1: # Miniboss is defeated
      self.dungeonMarkers['miniboss'].update(fill="#ADD8E6")

    if bossStatus: # Boss is defeated
      self.dungeonMarkers['miniboss'].update(fill="#ADD8E6")
      self.dungeonMarkers['boss'].update(fill="#ADD8E6")

    if bossFlags & 2: # Dungeon is totally complete
      self.dungeonMarkers['complete'].update(fill="#ADD8E6")
      self.dungeonMarkers['boss'].update(fill="#ADD8E6")
      self.dungeonMarkers['miniboss'].update(fill="#ADD8E6")
    
    if self.isOpen():
      self.dungeonMarkers['key'].update(fill="#ADD8E6")
    else:
      self.dungeonMarkers['key'].update(fill="#F08080")
    
    if self.hasItem():
      self.dungeonMarkers['item'].update(fill="#ADD8E6")
    else:
      self.dungeonMarkers['item'].update(fill="#F08080")
    
  def isOpen(self):
    if not self.level:
      return False
    return getOpenDungeons(self.zelda)[self.level-1]
    
  def hasItem(self):
    if not self.level:
      return False
    return getDungeonItems(self.zelda)[self.level-1]

  def reset(self):
    self.update(fill='#FFFFFF')
    self.update(text=self.name)
  
  def __repr__(self):
    if self.box:
      return f"{type(self).__name__} at {self.canvas.coords(self.box)}"
    else:
      return f"{type(self).__name__} at UNDEFINED"


class TailCave(DungeonItem):
  name = "Tail Cave"
  level = 1

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
