from lib.gui.widgets.tileMap import TileMap
from lib.gui.widgets.mycanvas import MyCanvas
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
import tkinter as tk

class FlagMap(TileMap):
  def __init__(self, canvas: MyCanvas, zelda:LinksAwakeningWrapper, x, y, boxSize, mapName="Flags:"):
    self.zelda = zelda
    super().__init__(canvas, x, y, boxSize, 10, 10, mapName)
    self.tips = {}
    self.tipLabel = self.canvas.draw_text(x, y+boxSize*11, "None")
    for coords, tile in self.tiles.items():
      self.tips[tile.box] = "None"
      self.canvas.tag_bind(tile.box, "<Enter>", self.testIn)
      # self.canvas.tag_bind(tile.box, "<Leave>", self.testOut)
      tile.update(fill="#880000")
    
  def testIn(self, event:tk.Event):
    wID = event.widget.find_withtag('current')[0]
    self.canvas.itemconfig(self.tipLabel, text=f"{self.tips[wID]}")
    
  def testOut(self, event:tk.Event):
    self.canvas.itemconfig(self.tipLabel, text=f"None")


  def update(self, tiles):
    for tY,r in enumerate(tiles):
      for tX,c in enumerate(r):
        if (tX,tY) not in self.tiles:
          continue
        self.tiles[(tX,tY)].update(fill=f"#{hex(c[0])[2:].zfill(2)*3}", text=hex(c[0])[2:].zfill(2))
        self.tips[self.tiles[(tX,tY)].box] = c[1]