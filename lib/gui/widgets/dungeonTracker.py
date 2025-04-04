from lib.gui.widgets.base import BaseWidget
from lib.gui.widgets.dungeonElements import *
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from lib.gui.widgets.mycanvas import MyCanvas
class DungeonTracker(BaseWidget):  
  def __init__(self, canvas: MyCanvas, zelda:LinksAwakeningWrapper, x, y, boxWidth, boxHeight):
    self.x = x
    self.y = y
    width  = boxWidth*3+10
    height = boxHeight*5+40
    self.canvas = canvas
    self.zelda = zelda
    self.canvas.draw_text(x, y, "Dungeons:")
    self.dungeons: list[DungeonItem] = [
      TailCave    (self.canvas, self.zelda, self.x+width*0, self.y+16+height*0, width, height),
      BottleGrotto(self.canvas, self.zelda, self.x+width*1, self.y+16+height*0, width, height),
      KeyCavern   (self.canvas, self.zelda, self.x+width*2, self.y+16+height*0, width, height),
      AnglersPond (self.canvas, self.zelda, self.x+width*3, self.y+16+height*0, width, height),
      CatfishMaw  (self.canvas, self.zelda, self.x+width*0, self.y+16+height*1, width, height),
      FaceShrine  (self.canvas, self.zelda, self.x+width*1, self.y+16+height*1, width, height),
      EaglesTower (self.canvas, self.zelda, self.x+width*2, self.y+16+height*1, width, height),
      TurtleRock  (self.canvas, self.zelda, self.x+width*3, self.y+16+height*1, width, height),
    ]

  def reset(self):
    for item in self.dungeons():
      item: DungeonItem
      item.reset()

  def update(self):
    for item in self.dungeons:
      item: DungeonItem
      item.update()