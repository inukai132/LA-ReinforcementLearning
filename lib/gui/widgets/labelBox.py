from lib.gui.widgets.base import BaseWidget
from lib.gui.widgets.mycanvas import MyCanvas

class LabelBox(BaseWidget):
  def __init__(self, canvas:MyCanvas, x, y, width, height, text='', fill='#FFFFFF', fontSize=10, fontColor="auto"):
    self.canvas = canvas
    self.x = x
    self.y = y
    self.width = width 
    self.height = height
    self.text = text
    self.fill = fill
    self.box  = None
    self.label = None
    self.fontSize = fontSize
    self.fontColor = fontColor
    self.effFontColor = '#000000'
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
      textX = bbox[0]+2
      textY = bbox[1]+2
    if self.label:
      self.canvas.moveto(self.label, textX, textY)
      self.canvas.itemconfig(self.label, text=self.text, fill=self.effFontColor)
    else:
      self.label = self.canvas.draw_text(textX, textY, self.text, fontColor=self.effFontColor, size=self.fontSize)


  def _updateFill(self, fill):
    self.fill = fill
    if self.fontColor == "auto":
      r,g,b = (int(x,16) for x in (self.fill[1:3],self.fill[3:5],self.fill[5:7]))
      lum = (0.299 * r + 0.587 * g + 0.114 * b)/255
      if lum < .5:
        self.effFontColor = '#FFFFFF'
      else:
        self.effFontColor = '#000000'

  def _updateText(self, text):
    self.text = text

  def update(self, fill=None, text=None):
    if fill is not None:
      self._updateFill(fill)
    if text is not None:
      self._updateText(text)
    self.draw()

  def draw(self):
    self.drawBox()
    self.drawLabel()

  def reset(self):
    self.draw()