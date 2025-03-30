import tkinter as tk
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from lib.gui.widgets.inventoryTracker import InventoryTracker
from lib.gui.widgets.dungeonTracker import DungeonTracker
from lib.gui.widgets.roomObjectMap import RoomObjectMap
from lib.gui.widgets.stateMap import StateMap
from lib.gui.widgets.subInventoryTracker import SubTracker
from lib.util.enums import *

class Window:

  LINK_COLOR = "#00CC00"
  ENTITY_COLORS = [
    "maroon", "olive", 
    "darkslateblue", "darkcyan", "steelblue", 
    "chocolate", "darkblue", "goldenrod", 
    "darkseagreen", "purple", "maroon3", "red", 
    "blueviolet", "crimson", "aqua", "blue", "greenyellow", 
    "orchid", "fuchsia", "dodgerblue", "salmon", "#ffff54", 
    "lightblue", "deeppink", "mediumslateblue", "palegreen", 
    "lightpink",
  ]
  NULL_COORDS = 10000

  # Send canvas elements here to "disable" them. This should be outside of the window geometry

  def __init__(self, zelda:LinksAwakeningWrapper, root:tk.Tk):
    self.zelda = zelda
    self.root = root

    self.root.geometry('800x600')
    self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
    self.canvas.pack(anchor=tk.CENTER, expand=True)

    self.box_size = 16

    self.roomObjects = RoomObjectMap(self.canvas, self.zelda, 5, 5, self.box_size)
    self.link = self.draw_triangle(self.LINK_COLOR)
    self.entities = [
      self.draw_diamond(e)
      for e in self.ENTITY_COLORS
    ]

    self.subTrack = SubTracker(self.canvas, self.zelda, 11*self.box_size, 15)
    
    rowOff = self.box_size*9+20
    self.canvas.create_text(self.box_size*1, rowOff, text="Inventory:", anchor=tk.NW)
    rowOff+=self.box_size

    self.inventory=InventoryTracker(self.canvas, self.zelda, self.box_size, rowOff, 75, 20)

    self.stairs = self.draw_triangle('brown')

    self.dungeons = DungeonTracker(self.canvas, self.zelda, 175, self.box_size*9+20, 50, 16)

    self.overworldState = StateMap(self.canvas, self.zelda, 275, 5, 8, "Overwold State:")

    self.interiorAState = StateMap(self.canvas, self.zelda, 275+8*17, 5, 8, "Interior A State:")

    self.interiorBState = StateMap(self.canvas, self.zelda, 275+8*34, 5, 8, "Interior B State:")

    self.curOver = self.canvas.create_oval(
      self.NULL_COORDS, self.NULL_COORDS, 
      self.NULL_COORDS+8, self.NULL_COORDS+8, fill=self.LINK_COLOR)

    self.curInt = self.canvas.create_oval(
      self.NULL_COORDS, self.NULL_COORDS, 
      self.NULL_COORDS+8, self.NULL_COORDS+8, fill=self.LINK_COLOR)

    self.score = self.canvas.create_text(20, 330, text="Score: <Loading>", anchor=tk.W)

    self.drawLoop()



  def draw_triangle(self, color='white'):
    return self.canvas.create_polygon(self.box_size//2,0,0,self.box_size,self.box_size,self.box_size,self.box_size//2,0,fill=color)

  def draw_diamond(self, color='white'):
    return self.canvas.create_polygon(
      self.box_size//2, 0,
      self.box_size,    self.box_size//2,
      self.box_size//2, self.box_size,
      0,                self.box_size//2,
      self.box_size//2, 0,
      fill=color)

  def rotateTri(self, tri, direct):
    points = self.canvas.coords(tri)
    x = points[0::2]
    y = points[1::2]

    bbox = [min(x),min(y),max(x),max(y)]

    match direct:
      case DIRECTION.DIRECTION_RIGHT.value:
        points = [
          bbox[0],bbox[1],
          bbox[2],(bbox[1]+bbox[3])//2,
          bbox[0],bbox[3],
          bbox[0],bbox[1]
        ]
      case DIRECTION.DIRECTION_LEFT.value:
        points = [
          bbox[2],bbox[1],
          bbox[0],(bbox[1]+bbox[3])//2,
          bbox[2],bbox[3],
          bbox[2],bbox[1]
        ]
      case DIRECTION.DIRECTION_UP.value:
        points = [
          bbox[0],bbox[3],
          bbox[2],bbox[3],
          (bbox[0]+bbox[2])//2,bbox[1],
          bbox[0],bbox[3]
        ]
      case DIRECTION.DIRECTION_DOWN.value:
        points = [
          bbox[0],bbox[1],
          bbox[2],bbox[1],
          (bbox[0]+bbox[2])//2,bbox[3],
          bbox[0],bbox[1]
        ]
    self.canvas.coords(tri, *points)


  def drawLoop(self):
    self.roomObjects.update()
    
    for e in self.entities:
      self.canvas.moveto(e, self.NULL_COORDS, self.NULL_COORDS)

    entities = self.zelda.getEntities()
    for i, e in enumerate(entities):
      if e.status == ENTITY_STATUS.ENTITY_STATUS_DISABLED.value:
        self.canvas.moveto(self.entities[i], self.NULL_COORDS, self.NULL_COORDS)
      else:
        tX, tY = self.entity2tileCoords(e.x, e.y)
        self.canvas.moveto(self.entities[i], tX, tY)

    l = self.zelda.getLinkStats()
    tX, tY = self.entity2tileCoords(l.x, l.y)
    self.canvas.moveto(self.link, tX, tY)

    self.subTrack.update()
    self.inventory.update()
    self.overworldState.update(self.zelda.getOverworldRoomStatus())
    self.interiorAState.update(self.zelda.getIndoorARoomStatus())
    self.interiorBState.update(self.zelda.getIndoorBRoomStatus())

    overID = l.overworldRoomID
    overX = (overID&0xF)*8-1
    overY = (overID>>4)*8-1
    self.canvas.moveto(self.curOver, self.overworldState.x+overX, self.overworldState.y+15+overY)

    if self.zelda.getFlags().isIndoors:
      if 6 <= l.mapID < 0x1a:
        interiorSet = 275+8*34
      else:
        interiorSet = 275+8*17
      innerID = l.mapRoom
      innerX = (innerID&0xf)*8-1+interiorSet
      innerY = (innerID>>4)*8-1+20
    else:
      innerX = self.NULL_COORDS
      innerY = self.NULL_COORDS

    self.canvas.moveto(self.curInt, innerX, innerY)

    stair = self.zelda.getCurrentStairs()
    tX, tY = self.entity2tileCoords(stair.x, stair.y)

    match stair.state:
      case STAIRCASE.STAIRCASE_NONE.value:
        self.canvas.moveto(self.stairs, self.NULL_COORDS, self.NULL_COORDS)
      case STAIRCASE.STAIRCASE_INACTIVE.value:
        self.canvas.moveto(self.stairs, tX, tY)
        self.canvas.itemconfig(self.stairs, fill="grey")
      case STAIRCASE.STAIRCASE_ACTIVE.value:
        self.canvas.moveto(self.stairs, tX, tY)
        self.canvas.itemconfig(self.stairs, fill="brown")
    
    self.dungeons.update()

    self.rotateTri(self.link, l.dir)

    self.canvas.itemconfig(self.score, text=f"Score: {self.getScore()}")

    self.canvas.after(1000//60, self.drawLoop)

  def entity2tileCoords(self, eX, eY):
    scale = self.box_size//16
    return (eX+8)*scale-self.box_size+5, (eY+1)*scale-self.box_size+18
  
  def getFrameScore(self):
    # Penalize spending time without making progress
    return -self.zelda.pyboy.frame_count

  def getRupeeScore(self):
    # Reward collecting rupees. This may need more tweaking
    return self.zelda.getRupees().count

  def getCurrentEntitiesScore(self):
    # Penalize number of entities on screen. The goal is to guide the player to killing enemies and collecting rewards
    activeEntities = [e for e in self.zelda.getEntities() if e.status != ENTITY_STATUS.ENTITY_STATUS_DISABLED.value]
    return len(activeEntities)*-10

  def getDungeonScore(self):
    # Reward dungeon progress
    score = 0
    for i,d in enumerate(self.zelda.getDungeonItems()):
      if self.dungeons.dungeons[i].isOpen():
        score += 1000
      if self.dungeons.dungeons[i].hasItem():
        score += 3000
      if d.beak:
        score += 200
      if d.compass:
        score += 400
      if d.map:
        score += 400
      if d.bossKey:
        score += 800
      if self.zelda.getBossFlags()[i] & 1:
        score += 4000
      if self.zelda.getBossStatus()[i] & 1:
        score += 6000
      if self.zelda.getBossFlags()[i] & 2:
        score += 8000
    return score
  
  def getMapScore(self):
    # Reward exploration, more score per room visited
    score = 0
    score += sum(50 for x in [self.zelda.getOverworldRoomStatus()] if x)
    score += sum(50 for x in [self.zelda.getIndoorARoomStatus()] if x)
    score += sum(50 for x in [self.zelda.getIndoorBRoomStatus()] if x)
    return score
  
  def getFlagsScore(self):
    # Reward story progression
    flags = self.zelda.getFlags()
    score = 0
    score += flags.lostInWoods * -1000
    score += flags.gelsStuck * -1000
    score += flags.shopItem1 * 1000
    score += flags.shopItem2 * 1000
    score += flags.shopItem3 * 1000
    score += flags.shopItem4 * 1000
    score += flags.marinStatus * 10000
    score += flags.eggMazeProg * 100000
    score += flags.hasFlippers * 10000
    score += flags.hasMedicine * 10000
    score += flags.hasTailKey * 10000
    score += flags.hasFishKey * 10000
    score += flags.hasFaceKey * 10000
    score += flags.hasBirdKey * 10000
    score += flags.hasSlimeKey * 10000
    score += flags.tarinStatus * 10000
    score += flags.songs * 10000
    score += flags.hasToadstool * 5000
    score += flags.richardSpoken * 10000
    score += flags.bowWow * 10000
    score += flags.marinFollows * 10000
    score += flags.marinInAnimalVil * 50000
    score += flags.ghostFollowing * 10000
    score += flags.ghostStep2 * 30000
    score += flags.roosterFollowing * 20000
    score += flags.eggMaze * 10000
    score += flags.finalForm * 100000
    score += flags.signpostMazeGoal * 10000
    score += flags.signpostMazeCur * 10000
    score += flags.powerup * 10000
    score += flags.tileGlint * 10000
    return score

  def getInventoryScore(self):
    # Reward having items, this includes having consumables and passive items
    score = 0
    inv = self.zelda.getInventory()
    score += inv.sword * 10000
    score += inv.shield * 10000
    score += inv.brace * 10000
    score += inv.ocarina * 10000

    score += inv.powder * 1000
    score += inv.bow * 1000
    score += inv.bombs * 1000
    
    score += inv.roc * 10000
    score += inv.boots * 10000
    score += inv.shovel * 10000
    score += inv.magicRod * 10000
    score += inv.hookshot * 10000
    
    score += inv.tradeItem * 10000
    score += inv.boomerang * 100000

    score += inv.flippers * 10000

    score += inv.tailKey * 2000
    score += inv.slimeKeyOrLeaves * 400
    score += inv.anglerKey * 2000
    score += inv.faceKey * 2000
    score += inv.birdKey * 2000

    score += inv.medicine * 10000
    score += inv.seashells * 1000
    score += inv.heartPieces * 2000

    return score

  def getHealthScore(self):
    return self.zelda.getCurHearts() * 1000

  def getScore(self):
    '''
    We want to reward progression without promoting loops or local maxima.
    No fixed range, everything will be relative. 
    '''
    score = self.getFrameScore() + self.getRupeeScore() + self.getCurrentEntitiesScore() + \
    self.getDungeonScore() + self.getMapScore() + self.getFlagsScore() + self.getHealthScore()


    return score


def startWindow(root:tk.Tk):
  root.mainloop()