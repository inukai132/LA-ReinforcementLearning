import tkinter as tk
from multiprocessing.managers import SyncManager
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper

class Window:

  LINK_COLOR = "#00CC00"

  def __init__(self, zelda:LinksAwakeningWrapper, canvas:tk.Canvas):
    self.zelda = zelda
    self.canvas = canvas

  def draw_block(self, x, y, color, size=16):
    self.canvas.create_rectangle(x,y,x+size,y+size,fill=color)

  def drawTileMap(self, ox=0, oy=0, box_size=16):
    scale = box_size/16
    self.canvas.delete("all")
    for y,r in enumerate(self.zelda.getRoomObjects()):
      if y > 9:
        continue
      for x,c in enumerate(r):
        if x > 11:
          continue
        self.draw_block((ox+x)*box_size, (oy+y)*box_size, f"#{hex(c)[2:]*3}", box_size)
      

    l = self.zelda.getLinkStats()
    self.draw_block((l['X']+8)*scale,(l['Y']-4)*scale, self.LINK_COLOR, box_size)
    self.canvas.after(1000//60, self.drawTileMap)


def startWindow(zelda):
  root = tk.Tk()
  root.geometry('800x600')

  canvas = tk.Canvas(root, width=600, height=400, bg='white')
  canvas.pack(anchor=tk.CENTER, expand=True)

  win = Window(zelda, canvas)
  win.drawTileMap()

  root.mainloop()