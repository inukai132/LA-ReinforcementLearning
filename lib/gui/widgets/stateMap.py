from lib.gui.widgets.tileMap import TileMap
import tkinter as tk
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper

class StateMap(TileMap):
  def __init__(self, canvas:tk.Canvas, zelda:LinksAwakeningWrapper, x, y, boxSize, mapName="Room States:"):
    self.zelda = zelda
    super().__init__(canvas, x, y, boxSize, 16, 16, mapName)
  
  def update(self, tiles=None):
    self.setTiles(tiles)