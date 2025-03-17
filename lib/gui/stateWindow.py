import tkinter as tk
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from lib.gui.widgets.inventoryTracker import InventoryTracker
from lib.gui.widgets.dungeonTracker import DungeonTracker
from lib.gui.widgets.roomObjectMap import RoomObjectMap
from lib.gui.widgets.stateMap import StateMap
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

    self.initTextStatus()
    
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

    self.drawLoop()

  def initTextStatus(self):
      colOff = 12
      rowOff = 15
      self.health_text = self.canvas.create_text(self.box_size*colOff, rowOff, text="Health: <Loading>", anchor=tk.W)
      rowOff+=15
      self.rupee_text = self.canvas.create_text(self.box_size*colOff,  rowOff, text="Rupees: <Loading>", anchor=tk.W)
      rowOff+=15
      self.bomb_text = self.canvas.create_text(self.box_size*colOff,   rowOff, text="Bombs: <Loading>", anchor=tk.W)
      rowOff+=15
      self.powder_text = self.canvas.create_text(self.box_size*colOff, rowOff, text="Powder: <Loading>", anchor=tk.W)
      rowOff+=15
      self.arrow_text = self.canvas.create_text(self.box_size*colOff,  rowOff, text="Arrows: <Loading>", anchor=tk.W)
      rowOff+=15
      self.shells_text = self.canvas.create_text(self.box_size*colOff, rowOff, text="Shells: <Loading>", anchor=tk.W)
      rowOff+=15
      self.poh_text = self.canvas.create_text(self.box_size*colOff,   rowOff, text="Heart Pieces: <Loading>", anchor=tk.W)
      rowOff+=15
      self.trade_text = self.canvas.create_text(self.box_size*colOff,   rowOff, text="Trade Item: <Loading>", anchor=tk.W)


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

    self.canvas.itemconfig(self.health_text, text=f"Health: {self.zelda.getCurHearts()/8}/{self.zelda.getMaxHearts()}")
    self.canvas.itemconfig(self.rupee_text, text=f"Rupees: {self.zelda.getRupees()}")
    self.canvas.itemconfig(self.bomb_text, text=f"Bombs: {self.zelda.getBombCount()}/{self.zelda.getMaxBombs()}")
    self.canvas.itemconfig(self.arrow_text, text=f"Arrows: {self.zelda.getArrowCount()}/{self.zelda.getMaxArrows()}")
    self.canvas.itemconfig(self.powder_text, text=f"Powder: {self.zelda.getPowderCount()}/{self.zelda.getMaxPowder()}")
    self.canvas.itemconfig(self.shells_text, text=f"Shells: {self.zelda.getSeashells()}")
    self.canvas.itemconfig(self.poh_text, text=f"Heart Pieces: {self.zelda.getHeartPieces()}")
    self.canvas.itemconfig(self.trade_text, text=f"Trade Item: {self.zelda.getTradeItem()}")

    self.inventory.update()
    self.overworldState.update(self.zelda.getOverworldRoomStatus())
    self.interiorAState.update(self.zelda.getIndoorARoomStatus())
    self.interiorBState.update(self.zelda.getIndoorBRoomStatus())

    overID = l.overworldRoomID
    overX = (overID&0xF)*8-1
    overY = (overID>>4)*8-1
    self.canvas.moveto(self.curOver, self.overworldState.x+overX, self.overworldState.y+15+overY)

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

    self.canvas.after(1000//60, self.drawLoop)

  def entity2tileCoords(self, eX, eY):
    scale = self.box_size//16
    return (eX+8)*scale-self.box_size+5, (eY+1)*scale-self.box_size+20


def startWindow(zelda):
  root = tk.Tk()
  win = Window(zelda, root)

  root.mainloop()