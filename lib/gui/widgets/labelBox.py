import tkinter as tk
from lib.gui.widgets.base import BaseWidget

class LabelBox(BaseWidget):
  def __init__(self, canvas:tk.Canvas, x, y, width, height, text='', fill='white'):
    self.canvas = canvas
    self.x = x
    self.y = y
    self.width = width 
    self.height = height
    self.text = text
    self.fill = fill
    self.box  = None
    self.label = None
    self.draw()

  def drawBox(self):
    boxX0     = self.x
    boxY0     = self.y
    boxX1     = self.x+self.width
    boxY1     = self.y+self.height
    if self.box:
      self.canvas.coords(self.box, 
                             boxX0, boxY0,
                             boxX1, boxY1)
      self.canvas.itemconfig(self.box, fill=self.fill)
    else:
      self.box  = self.canvas.create_rectangle(
                  boxX0, boxY0, 
                  boxX1, boxY1, 
                  fill=self.fill)
  
  def drawLabel(self):
    if not self.box:
      textX = self.x
      textY = self.y
    else:
      bbox = self.canvas.bbox(self.box)
      textX = bbox[0] + 5
      textY = bbox[1] + (self.height-12)//2
    if self.label:
      self.canvas.moveto(self.label, textX, textY)
      self.canvas.itemconfig(self.label, text=self.text)
    else:
      self.label = self.canvas.create_text(textX, textY, text=self.text, anchor=tk.NW)

  def updateFill(self, fill):
    self.fill = fill
    self.drawBox()

  def updateText(self, text):
    self.text = text
    self.drawLabel()

  def draw(self):
    self.drawBox()
    self.drawLabel()

  def reset(self):
    self.draw()