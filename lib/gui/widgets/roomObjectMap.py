from lib.gui.widgets.tileMap import TileMap
import tkinter as tk
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper

class RoomObjectMap(TileMap):
  def __init__(self, canvas:tk.Canvas, zelda:LinksAwakeningWrapper, x, y, boxSize, mapName="Current Screen:"):
    self.zelda = zelda
    super().__init__(canvas, x, y, boxSize, 10, 8, mapName)
  
  def update(self):
    tiles = self.zelda.getRoomObjects()
    tiles = [
      [
        t for i,t in enumerate(r) if i and i <= self.dims[0]
      ]
      for j,r in enumerate(tiles) if j and j <= self.dims[1]
    ]
    tiles = self.remapTiles(tiles)
    self.setTiles(tiles)

  def remapTiles(self, tileList:list[list[int]])->list[list[int]]:
    tileset = set()
    for r in tileList:
      for c in r:
        tileset.add(c)
    
    sortTiles = list(tileset)
    sortTiles.sort(reverse=True)
    points = len(tileset)
    space = 255//points
    tileMap = {p:(i+1)*space for i,p in enumerate(sortTiles)}
    return [
      [
        tileMap[t] for t in r
      ] for r in tileList
    ]