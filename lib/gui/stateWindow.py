import tkinter as tk
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from lib.gui.widgets.inventoryTracker import InventoryTracker
from lib.gui.widgets.dungeonTracker import DungeonTracker
from lib.gui.widgets.roomObjectMap import RoomObjectMap
from lib.gui.widgets.stateMap import StateMap
from lib.gui.widgets.flagMap import FlagMap
from lib.gui.widgets.subInventoryTracker import SubTracker
from lib.util.enums import *
from lib.gui.widgets.mycanvas import MyCanvas

class Window:

  LINK_COLOR = "#00CC00"
  ENTITY_COLORS = [
    "#800000", "#808000", "#483D8B", "#97FFFF", 
    "#528B8B", "#D2691E", "#00688B", "#DAA520", 
    "#8FBC8F", "#800080", "#CD2990", "#FF0000", 
    "#8A2BE2", "#DC143C", "#00FFFF", "#0000FF", 
    "#ADFF2F", "#DA70D6", "#8B0A50", "#1E90FF", 
    "#FA8072", "#ffff54", "#ADD8E6", "#FF1493", 
    "#7B68EE", "#98FB98", "#FFB6C1", "#C5C1AA"
    
  ]
  NULL_COORDS = 10000
  MAP_STATE_SIZE=16
  FLAG_SIZE=16
  # Send canvas elements here to "disable" them. This should be outside of the window geometry

  def __init__(self, zelda:LinksAwakeningWrapper, root:tk.Tk):
    self.zelda = zelda
    self.drawing = False
    self.root = root
    self.root.geometry('1280x1024')
    self.canvas = MyCanvas(self.root, width=1280, height=1024, bg='#FFFFFF')
    self.canvas.pack(anchor=tk.CENTER, expand=True)

    self.box_size = 16

    self.roomObjects = RoomObjectMap(self.canvas, self.zelda, 5, 5, self.box_size)
    self.link = self.canvas.draw_triangle(self.box_size, self.LINK_COLOR)
    self.entities = [
      self.canvas.draw_diamond(self.box_size, e)
      for e in self.ENTITY_COLORS
    ]

    self.subTrack = SubTracker(self.canvas, self.zelda, 11*self.box_size, 15)
    
    rowOff = self.box_size*9+20
    self.canvas.draw_text(self.box_size*1, rowOff, "Inventory:")
    rowOff+=self.box_size

    self.inventory=InventoryTracker(self.canvas, self.zelda, self.box_size, rowOff, 75, 20)

    self.stairs = self.canvas.draw_triangle(self.box_size, '#9C661F')

    self.warps = [self.canvas.create_oval(self.NULL_COORDS, self.NULL_COORDS, self.NULL_COORDS+self.box_size, self.NULL_COORDS+self.box_size, fill='#FFFF00') for _ in range(4)]

    self.dungeons = DungeonTracker(self.canvas, self.zelda, 190, self.box_size*9+200, 50, 16)

    self.overworldState = StateMap(self.canvas, self.zelda, 300, 5, self.MAP_STATE_SIZE, "Overwold State:")

    self.interiorAState = StateMap(self.canvas, self.zelda, 300+self.MAP_STATE_SIZE*18, 5, self.MAP_STATE_SIZE, "Interior A State:")

    self.interiorBState = StateMap(self.canvas, self.zelda, 300+self.MAP_STATE_SIZE*36, 5, self.MAP_STATE_SIZE, "Interior B State:")
    self.drawing = True

    self.curOver = self.canvas.create_oval(
      self.NULL_COORDS, self.NULL_COORDS, 
      self.NULL_COORDS+self.MAP_STATE_SIZE, self.NULL_COORDS+self.MAP_STATE_SIZE, fill=self.LINK_COLOR)

    self.curInt = self.canvas.create_oval(
      self.NULL_COORDS, self.NULL_COORDS, 
      self.NULL_COORDS+self.MAP_STATE_SIZE, self.NULL_COORDS+self.MAP_STATE_SIZE, fill=self.LINK_COLOR)

    self.score = self.canvas.draw_text(20, 330, text="Score: <Loading>")

    self.flagState = FlagMap(self.canvas, self.zelda, 15, 346, self.FLAG_SIZE)

    self.drawLoop()

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
    overX = (overID&0xF)*self.MAP_STATE_SIZE-1
    overY = (overID>>4)*self.MAP_STATE_SIZE-1
    self.canvas.moveto(self.curOver, self.overworldState.x+overX, self.overworldState.y+15+overY)

    if self.zelda.getFlags().isIndoors:
      if 6 <= l.mapID < 0x1a:
        interiorSet = 275+self.MAP_STATE_SIZE*36
      else:
        interiorSet = 275+self.MAP_STATE_SIZE*18
      innerID = l.mapRoom
      innerX = (innerID&0xf)*self.MAP_STATE_SIZE-1+interiorSet
      innerY = (innerID>>4) *self.MAP_STATE_SIZE-1+20
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
        self.canvas.itemconfig(self.stairs, fill="#808080")
      case STAIRCASE.STAIRCASE_ACTIVE.value:
        self.canvas.moveto(self.stairs, tX, tY)
        self.canvas.itemconfig(self.stairs, fill="#9C661F")
    
    # for i,w in enumerate(self.zelda.getRoomWarps()):
    #   tX, tY = self.entity2tileCoords(w.X, w.Y)
    #   if w.map == 0:
    #     tX, tY = self.NULL_COORDS, self.NULL_COORDS
    #   self.canvas.moveto(self.warps[i], tX+8, tY+8)

    self.dungeons.update()

    self.canvas.rotateTri(self.link, l.dir)

    self.canvas.itemconfig(self.score, text=f"Score: {self.zelda.getScore():.2f}")

    flags = [(b,f"{a}\n{b}") for a,b in self.zelda.getFlags().__dict__.items()]
    flagMap = [
      [x for x in flags[10*i:10*i+10]] for i in range(10)
    ]

    self.flagState.update(flagMap)

    self.canvas.after(1000//200, self.drawLoop)

  def entity2tileCoords(self, eX, eY):
    scale = self.box_size//16
    return (eX+8)*scale-self.box_size+5, (eY+1)*scale-self.box_size+18


def startWindow(zelda:LinksAwakeningWrapper):
  root = tk.Tk()
  window = Window(zelda, root)
  root.mainloop()