from lib.gui.widgets.base import BaseWidget
from lib.gui.widgets.mycanvas import MyCanvas
from lib.gui.widgets.labelBox import LabelBox

class TileMap(BaseWidget):

  def __init__(self, canvas:MyCanvas, x, y, boxSize, tileWidth, tileHeight, mapName="Tile Map"):
    self.x = x
    self.y = y
    self.canvas = canvas
    self.box_size = boxSize
    self.dims = (tileWidth, tileHeight)

    self.canvas.draw_text(x, y, mapName)
    yOff = 15

    self.tiles = {}

    for tY in range(tileHeight):
      for tX in range(tileWidth):
        self.tiles[(tX,tY)] = LabelBox(self.canvas, self.x+tX*self.box_size, self.y+yOff+tY*self.box_size, self.box_size, self.box_size, "FF", fontSize=8)
        
  
  def update(self, tiles):
    for tY,r in enumerate(tiles):
      for tX,c in enumerate(r):
        if (tX,tY) not in self.tiles:
          continue
        try:
          self.tiles[(tX,tY)].update(text=hex(c)[2:].zfill(2).upper(), fill=f"#{hex(c)[2:].zfill(2)*3}")
        except Exception:
          self.tiles[(tX,tY)].update(text="??", fill="#ff0000")

      
