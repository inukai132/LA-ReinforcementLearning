from lib.gui.widgets.base import BaseWidget
from lib.gui.widgets.dungeonElements import *
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from tkinter import Canvas
class SubTracker(BaseWidget):  
  def __init__(self, canvas: Canvas, zelda:LinksAwakeningWrapper, x, y):
    self.x = x
    self.y = y
    self.canvas = canvas
    self.zelda = zelda
    self.canvas.create_text(x, y, text="Sub-Tracker: ", anchor=tk.W)
    offX = self.x+10
    offY = self.y+15
    self.health_text = self.canvas.create_text(offX, offY, text="Health: <Loading>", anchor=tk.W)
    offY+=15
    self.rupee_text = self.canvas.create_text(offX,  offY, text="Rupees: <Loading>", anchor=tk.W)
    offY+=15
    self.bomb_text = self.canvas.create_text(offX,   offY, text="Bombs: <Loading>", anchor=tk.W)
    offY+=15
    self.powder_text = self.canvas.create_text(offX, offY, text="Powder: <Loading>", anchor=tk.W)
    offY+=15
    self.arrow_text = self.canvas.create_text(offX,  offY, text="Arrows: <Loading>", anchor=tk.W)
    offY+=15
    self.shells_text = self.canvas.create_text(offX, offY, text="Shells: <Loading>", anchor=tk.W)
    offY+=15
    self.poh_text = self.canvas.create_text(offX,   offY, text="Heart Pieces: <Loading>", anchor=tk.W)
    offY+=15
    self.trade_text = self.canvas.create_text(offX,   offY, text="Trade Item: <Loading>", anchor=tk.W)
  
  def update(self):
    self.canvas.itemconfig(self.health_text, text=f"Health: {self.zelda.getCurHearts()/8}/{self.zelda.getMaxHearts()}")
    self.canvas.itemconfig(self.rupee_text, text=f"Rupees: {self.zelda.getRupees()}")
    self.canvas.itemconfig(self.bomb_text, text=f"Bombs: {self.zelda.getBombCount()}/{self.zelda.getMaxBombs()}")
    self.canvas.itemconfig(self.arrow_text, text=f"Arrows: {self.zelda.getArrowCount()}/{self.zelda.getMaxArrows()}")
    self.canvas.itemconfig(self.powder_text, text=f"Powder: {self.zelda.getPowderCount()}/{self.zelda.getMaxPowder()}")
    self.canvas.itemconfig(self.shells_text, text=f"Shells: {self.zelda.getSeashells()}")
    self.canvas.itemconfig(self.poh_text, text=f"Heart Pieces: {self.zelda.getHeartPieces()}")
    self.canvas.itemconfig(self.trade_text, text=f"Trade Item: {self.zelda.getTradeItem()}")