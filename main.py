import json
from pyboy import PyBoy
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from threading import Thread
from multiprocessing import Manager
from lib.gui.stateWindow import startWindow
from pathlib import Path
from lib.util.input_enum import PYBOY_INPUT

if __name__ == "__main__":
  rom = "res/la.gb"
  pb = PyBoy(rom, scale=4, record_input=True)
  pb.set_emulation_speed(1)
  print(pb.cartridge_title)
  zelda = LinksAwakeningWrapper(pb)
  
  ui = Thread(target=startWindow, args=(zelda,))
  ui.start()

  WINDOW_SIZE = 60*60*1

  i=0
  lastChunk = {}
  fullHistory = []
  while pb.tick():
    inputs = pb.events
    lastChunk.update({
      i:(inputs,zelda.getScore())
    })
    i+=1
    if i%WINDOW_SIZE == 0:
      lc = [(f, ts[1], PYBOY_INPUT(t._WindowEvent__event))for f,ts in lastChunk.items() for t in ts[0] if 0<t._WindowEvent__event<17]
      fullHistory += lc
      json.dump(lc,           Path(f"./res/inputs/{i-WINDOW_SIZE}_{i}.json").open('w'))
      json.dump(fullHistory,  Path("./res/inputs/fullHistory.json").open('w'))

      
