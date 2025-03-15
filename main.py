from pyboy import PyBoy
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from threading import Thread
from multiprocessing import Manager
from lib.gui.stateWindow import startWindow

def refreshWindow(zelda:LinksAwakeningWrapper):
  import time
  while True:
    time.sleep(1/24)
    zelda.drawStats()

if __name__ == "__main__":
  rom = "la.gb"
  pb = PyBoy(rom)
  pb.set_emulation_speed(1)
  print(pb.cartridge_title)
  zelda = LinksAwakeningWrapper(pb)
  mgr = Manager()
  ui = Thread(target=startWindow, args=(zelda,))
  ui.start()
  zelda.start_game()
  pb.screen.image.show()
  print(zelda.base)