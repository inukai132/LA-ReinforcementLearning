from lib.gui.widgets.base import BaseWidget
import tkinter as tk

class TileMap(BaseWidget):

  def __init__(self, canvas: tk.Canvas, x, y, boxSize, tileWidth, tileHeight, mapName="Tile Map"):
    self.x = x
    self.y = y
    self.canvas = canvas
    self.box_size = boxSize
    self.dims = (tileWidth, tileHeight)

    self.canvas.create_text(x, y, text=mapName, anchor=tk.NW)
    yOff = 15

    self.tiles = {}

    for tY in range(tileHeight):
      for tX in range(tileWidth):
        self.tiles[(tX,tY)] = self.canvas.create_rectangle(
          self.x+tX*self.box_size, self.y+yOff+tY*self.box_size,
          self.x+(tX+1)*self.box_size, self.y+yOff+(tY+1)*self.box_size,
          fill='black')
  
  def setTiles(self, tiles):
    for tY,r in enumerate(tiles):
      for tX,c in enumerate(r):
        self.canvas.itemconfig(self.tiles[(tX,tY)],fill=f"#{hex(c)[2:]*3}")

      
