import tkinter as tk

class MyCanvas(tk.Canvas):
  
  def draw_text(self, x, y, text, anchor=tk.NW, font="Consolas", size=10, fontColor="black"):
    return self.create_text(x, y, text=text, anchor=anchor, font=(font,size), fill=fontColor)

  def draw_triangle(self, box_size, color='#FFFFFF'):
    return self.create_polygon(box_size//2,0,0,box_size,box_size,box_size,box_size//2,0,fill=color)

  def draw_diamond(self, box_size, color='#FFFFFF'):
    return self.create_polygon(
      box_size//2, 0,
      box_size,    box_size//2,
      box_size//2, box_size,
      0,           box_size//2,
      box_size//2, 0,
      fill=color)

  def rotateTri(self, tri, direct):
    from lib.util.enums import DIRECTION
    points = self.coords(tri)
    x = points[0::2]
    y = points[1::2]

    bbox = [min(x),min(y),max(x),max(y)]

    match direct:
      case DIRECTION.DIRECTION_RIGHT.value:
        points = [
          bbox[0],bbox[1],
          bbox[2],(bbox[1]+bbox[3])//2,
          bbox[0],bbox[3],
          bbox[0],bbox[1]
        ]
      case DIRECTION.DIRECTION_LEFT.value:
        points = [
          bbox[2],bbox[1],
          bbox[0],(bbox[1]+bbox[3])//2,
          bbox[2],bbox[3],
          bbox[2],bbox[1]
        ]
      case DIRECTION.DIRECTION_UP.value:
        points = [
          bbox[0],bbox[3],
          bbox[2],bbox[3],
          (bbox[0]+bbox[2])//2,bbox[1],
          bbox[0],bbox[3]
        ]
      case DIRECTION.DIRECTION_DOWN.value:
        points = [
          bbox[0],bbox[1],
          bbox[2],bbox[1],
          (bbox[0]+bbox[2])//2,bbox[3],
          bbox[0],bbox[1]
        ]
    self.coords(tri, *points)