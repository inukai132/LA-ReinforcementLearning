from pyboy import PyBoy
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from threading import Thread
from multiprocessing import Manager
from lib.gui.stateWindow import startWindow
from pathlib import Path

if __name__ == "__main__":
  rom = "res/la.gb"
  pb = PyBoy(rom)
  pb.set_emulation_speed(1)
  print(pb.cartridge_title)
  zelda = LinksAwakeningWrapper(pb)
  mgr = Manager()
  ui = Thread(target=startWindow, args=(zelda,))
  ui.start()
  while pb.tick():
    pass

  # zelda.start_game()
  # pb.screen.image.show()
  # print(zelda.base)