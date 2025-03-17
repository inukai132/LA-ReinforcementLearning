from lib.gui.widgets.base import BaseWidget
from lib.gui.widgets.inventoryElements import *
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from tkinter import Canvas
class InventoryTracker(BaseWidget):  
  def __init__(self, canvas: Canvas, zelda:LinksAwakeningWrapper, x, y, boxWidth, boxHeight):
    self.x = x
    self.y = y
    self.canvas = canvas
    self.zelda = zelda
    self.items: list[InventoryItem] = []
    self.items.append(SwordItem   (canvas, zelda, x+boxWidth*(1-1), y+boxHeight*(1-1), boxWidth, boxHeight))
    self.items.append(PowderItem  (canvas, zelda, x+boxWidth*(1-1), y+boxHeight*(2-1), boxWidth, boxHeight))
    self.items.append(BowItem     (canvas, zelda, x+boxWidth*(1-1), y+boxHeight*(3-1), boxWidth, boxHeight))
    self.items.append(ShovelItem  (canvas, zelda, x+boxWidth*(1-1), y+boxHeight*(4-1), boxWidth, boxHeight))
    self.items.append(BombsItem   (canvas, zelda, x+boxWidth*(1-1), y+boxHeight*(5-1), boxWidth, boxHeight))
    self.items.append(BootsItem   (canvas, zelda, x+boxWidth*(1-1), y+boxHeight*(6-1), boxWidth, boxHeight))
    self.items.append(BraceItem   (canvas, zelda, x+boxWidth*(1-1), y+boxHeight*(7-1), boxWidth, boxHeight))
    self.items.append(ShieldItem  (canvas, zelda, x+boxWidth*(2-1), y+boxHeight*(1-1), boxWidth, boxHeight))
    self.items.append(RocItem     (canvas, zelda, x+boxWidth*(2-1), y+boxHeight*(2-1), boxWidth, boxHeight))
    self.items.append(HookshotItem(canvas, zelda, x+boxWidth*(2-1), y+boxHeight*(3-1), boxWidth, boxHeight))
    self.items.append(OcarinaItem (canvas, zelda, x+boxWidth*(2-1), y+boxHeight*(4-1), boxWidth, boxHeight))
    self.items.append(BoomerngItem(canvas, zelda, x+boxWidth*(2-1), y+boxHeight*(5-1), boxWidth, boxHeight))
    self.items.append(MagicrodItem(canvas, zelda, x+boxWidth*(2-1), y+boxHeight*(6-1), boxWidth, boxHeight))

  def reset(self):
    for item in self.items():
      item: InventoryItem
      item.reset()

  def update(self):
    for item in self.items:
      item: InventoryItem
      item.update()