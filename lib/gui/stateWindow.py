import tkinter as tk
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
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

  ITEMS=[
        '', 'Swd', 'Bmb', 'Brc', 'Shd', 'Bow', 'Hks', 'MRd',
        'Bts', 'Ocr', 'Roc', 'Shv', 'Pow', 'Brg', '', ''
      ]

  # Send canvas elements here to "disable" them. This should be outside of the window geometry
  NULL_COORDS = 10000

  def drawBox(self, x, y, width=0, height=0, text=''):
    if not width:
      width = self.box_size
    if not height:
      height = self.box_size
    boxX1 = x
    boxX2 = x+width
    boxY1  = y
    boxY2  = y+height
    box = self.canvas.create_rectangle(boxX1, boxY1, boxX2, boxY2, fill='white')
    textX = x+width//2
    textY = y+height//2
    text = self.canvas.create_text(textX, textY, text=text)
    return box, text

  def __init__(self, zelda:LinksAwakeningWrapper, root:tk.Tk):
    self.zelda = zelda
    self.root = root

    self.root.geometry('800x600')
    self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
    self.canvas.pack(anchor=tk.CENTER, expand=True)

    self.box_size = 16

    self.mapTiles = [
      self.canvas.create_rectangle(self.NULL_COORDS,self.NULL_COORDS,self.NULL_COORDS+self.box_size,self.NULL_COORDS+self.box_size,fill='black')
      for _ in range(16*16)
    ]
    self.link = self.canvas.create_rectangle(self.NULL_COORDS,self.NULL_COORDS,self.NULL_COORDS+self.box_size,self.NULL_COORDS+self.box_size,fill=self.LINK_COLOR)
    self.entities = [
      self.canvas.create_rectangle(self.NULL_COORDS,self.NULL_COORDS,self.NULL_COORDS+self.box_size,self.NULL_COORDS+self.box_size,fill=e)
      for e in self.ENTITY_COLORS
    ]

    self.initTextStatus()
    
    rowOff = 140
    self.canvas.create_text(self.box_size*1, rowOff, text="Inventory:", anchor=tk.W)
    rowOff+=15

    self.inventory={
      self.ITEMS[7*x+y+1]:self.drawBox(self.box_size*(2*x+1), rowOff+(y*self.box_size), self.box_size*2, self.box_size, self.ITEMS[7*x+y+1])
      for x in range(2)
      for y in range(7)
    }

    self.stairs = self.canvas.create_polygon(self.box_size//2,0,0,self.box_size,self.box_size,self.box_size,self.box_size//2,0,fill="brown")

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

  def drawLoop(self):
    for e in self.mapTiles:
      self.canvas.moveto(e, self.NULL_COORDS, self.NULL_COORDS)
    
    roomObjects = self.zelda.getRoomObjects()
    for y,r in enumerate(roomObjects):
      if y >= 9:
        continue
      if y == 0:
        continue
      for x,c in enumerate(r):
        if x == 0:
          continue
        if x >= 11:
          continue
        tileX = x*self.box_size-self.box_size
        tileY = y*self.box_size-self.box_size
        newFill = f"#{hex(c)[2:].zfill(2)*3}"
        tile = self.mapTiles[y*16+x]
        self.canvas.itemconfig(tile, fill=newFill)
        self.canvas.moveto(tile, tileX, tileY)
    
    for e in self.entities:
      self.canvas.moveto(e, self.NULL_COORDS, self.NULL_COORDS)

    entities = self.zelda.getEntities()
    for i, e in enumerate(entities):
      if e.status == ENTITY_STATUS.ENTITY_STATUS_DISABLED.value:
        self.canvas.moveto(self.entities[i], self.NULL_COORDS, self.NULL_COORDS)
      else:
        self.canvas.moveto(self.entities[i], e.x+8-self.box_size, e.y-self.box_size)

    l = self.zelda.getLinkStats()
    self.canvas.moveto(self.link, l.x+8-self.box_size, l.y-4-self.box_size)

    self.canvas.itemconfig(self.health_text, text=f"Health: {self.zelda.getCurHearts()/8}/{self.zelda.getMaxHearts()}")
    self.canvas.itemconfig(self.rupee_text, text=f"Rupees: {self.zelda.getRupees()}")
    self.canvas.itemconfig(self.bomb_text, text=f"Bombs: {self.zelda.getBombCount()}/{self.zelda.getMaxBombs()}")
    self.canvas.itemconfig(self.arrow_text, text=f"Arrows: {self.zelda.getArrowCount()}/{self.zelda.getMaxArrows()}")
    self.canvas.itemconfig(self.powder_text, text=f"Powder: {self.zelda.getPowderCount()}/{self.zelda.getMaxPowder()}")
    self.canvas.itemconfig(self.shells_text, text=f"Shells: {self.zelda.getSeashells()}")
    self.canvas.itemconfig(self.poh_text, text=f"Heart Pieces: {self.zelda.getHeartPieces()}")
    self.canvas.itemconfig(self.trade_text, text=f"Trade Item: {self.zelda.getTradeItem()}")

    for item in self.inventory.values():
      self.canvas.itemconfig(item[0], fill='pink')  

    for item in self.zelda.getInventory():
      if self.ITEMS[item]:
        self.canvas.itemconfig(self.inventory[self.ITEMS[item]][0], fill='lightgreen')

    for item in self.zelda.getCurrentEquip():
      if self.ITEMS[item]:
        self.canvas.itemconfig(self.inventory[self.ITEMS[item]][0], fill='lightblue')

    self.canvas.itemconfig(self.inventory['Swd'][1], text=f"Swd {self.zelda.getSwordLevel()}")
    self.canvas.itemconfig(self.inventory['Shd'][1], text=f"Shd {self.zelda.getShieldLevel()}")
    self.canvas.itemconfig(self.inventory['Brc'][1], text=f"Brc {self.zelda.getBraceletLevel()}")
    self.canvas.itemconfig(self.inventory['Ocr'][1], text=f"Ocr {self.zelda.getCurSong()}")
    
    stair = self.zelda.getCurrentStairs()

    match stair.state:
      case STAIRCASE.STAIRCASE_NONE.value:
        self.canvas.moveto(self.stairs, self.NULL_COORDS, self.NULL_COORDS)
      case STAIRCASE.STAIRCASE_INACTIVE.value:
        self.canvas.moveto(self.stairs, stair.x-self.box_size//2, stair.y-self.box_size)
        self.canvas.itemconfig(self.stairs, fill="grey")
      case STAIRCASE.STAIRCASE_ACTIVE.value:
        self.canvas.moveto(self.stairs, stair.x-self.box_size//2, stair.y-self.box_size)
        self.canvas.itemconfig(self.stairs, fill="brown")
    
      

    self.canvas.after(1000//60, self.drawLoop)


def startWindow(zelda):
  root = tk.Tk()
  win = Window(zelda, root)

  root.mainloop()