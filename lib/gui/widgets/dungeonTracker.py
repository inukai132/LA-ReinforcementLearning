from lib.gui.widgets.base import BaseWidget
from lib.gui.widgets.dungeonElements import *
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from tkinter import Canvas
class DungeonTracker(BaseWidget):  
  def __init__(self, canvas: Canvas, zelda:LinksAwakeningWrapper, x, y, boxWidth, boxHeight):
    self.x = x
    self.y = y
    width  = boxWidth*3+10
    height = boxHeight*5+40
    self.canvas = canvas
    self.zelda = zelda
    self.canvas.create_text(x, y, text="Dungeons:", anchor=tk.NW)
    y+=16
    self.dungeons: list[DungeonItem] = [
      TailCave    (canvas, zelda, x+width*0, y+height*0, width, height),
      BottleGrotto(canvas, zelda, x+width*1, y+height*0, width, height),
      KeyCavern   (canvas, zelda, x+width*2, y+height*0, width, height),
      AnglersPond (canvas, zelda, x+width*3, y+height*0, width, height),
      CatfishMaw  (canvas, zelda, x+width*0, y+height*1, width, height),
      FaceShrine  (canvas, zelda, x+width*1, y+height*1, width, height),
      EaglesTower (canvas, zelda, x+width*2, y+height*1, width, height),
      TurtleRock  (canvas, zelda, x+width*3, y+height*1, width, height),
    ]

  def reset(self):
    for item in self.dungeons():
      item: DungeonItem
      item.reset()

  def update(self):
    for item in self.dungeons:
      item: DungeonItem
      item.update()