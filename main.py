import json
from pyboy import PyBoy
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from threading import Thread
from multiprocessing import Manager
from lib.gui.stateWindow import Window, startWindow
from pathlib import Path
from lib.util.input_enum import PYBOY_INPUT
import tkinter as tk

if __name__ == "__main__":
  rom = "res/la.gb"
  pb = PyBoy(rom, scale=4, record_input=True)
  pb.set_emulation_speed(1)
  print(pb.cartridge_title)
  zelda = LinksAwakeningWrapper(pb)

  root = tk.Tk()
  win = Window(zelda, root)  
  
  ui = Thread(target=startWindow)
  ui.start()

  WINDOW_SIZE = 60*60*1

  i=0
  lastChunk = {}
  fullHistory = []
  while pb.tick():
    inputs = pb.events
    lastChunk.update({
      i:(inputs,win.getScore())
    })
    i+=1
    if i%WINDOW_SIZE == 0:
      lc = [(f, t[1], PYBOY_INPUT(t[0]))for f,ts in lastChunk.items() for t in ts if 0<t[0]<17]
      fullHistory += lc
      json.dump(lc,           Path(f"./inputs/{i-WINDOW_SIZE}_{i}.json").open('w'))
      json.dump(fullHistory,  Path("./fullHistory.json").open('w'))

      
