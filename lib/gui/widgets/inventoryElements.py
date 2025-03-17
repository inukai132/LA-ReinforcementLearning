from lib.gui.widgets.labelBox import LabelBox
from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper
from lib.util.enums import INVENTORY

class InventoryItem(LabelBox):
  name = "UNK"

  def __init__(self, canvas, zelda, x, y, width, height):
    self.zelda = zelda
    self.canvas = canvas
    super().__init__(canvas, x, y, width, height, f"{self.name} ?", 'white')
  
  def update(self):
    newText = f"{self.name} {self.getNewText()}"
    if len(newText) > 10:
      newText = newText[:10]
    self.updateText(newText)
    
    newColor = self.getNewColor()
    self.updateFill(newColor)    

  def reset(self):
    self.updateFill('white')
    self.updateText(self.name)
  
  def __repr__(self):
    if self.box:
      return f"{type(self).__name__} at {self.canvas.coords(self.box)}"
    else:
      return f"{type(self).__name__} at UNDEFINED"
    
  def getNewColor(self):
    if self.itemID in self.zelda.getCurrentEquip():
      return 'lightblue'
    if getattr(self.zelda.getInventory(),self.name,0):
      return 'lightgreen'
    return 'pink'


class SwordItem(InventoryItem):
  name = "sword"
  itemID = INVENTORY.INVENTORY_SWORD.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return str(self.zelda.getSwordLevel())
    

class ShieldItem(InventoryItem):
  name = "shield"
  itemID = INVENTORY.INVENTORY_SHIELD.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return str(self.zelda.getShieldLevel())
    

class PowderItem(InventoryItem):
  name = "powder"
  itemID = INVENTORY.INVENTORY_MAGIC_POWDER.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return str(self.zelda.getPowderCount())
    

class RocItem(InventoryItem):
  name = "roc"
  itemID = INVENTORY.INVENTORY_ROCS_FEATHER.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return ""
    

class BombsItem(InventoryItem):
  name = "bombs"
  itemID = INVENTORY.INVENTORY_BOMBS.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return str(self.zelda.getBombCount())

class BootsItem(InventoryItem):
  name = "boots"
  itemID = INVENTORY.INVENTORY_PEGASUS_BOOTS.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return ""
    

class BraceItem(InventoryItem):
  name = "brace"
  itemID = INVENTORY.INVENTORY_POWER_BRACELET.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return str(self.zelda.getBraceletLevel())
    

class BowItem(InventoryItem):
  name = "bow"
  itemID = INVENTORY.INVENTORY_BOW.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return str(self.zelda.getArrowCount())
    

class ShovelItem(InventoryItem):
  name = "shovel"
  itemID = INVENTORY.INVENTORY_SHOVEL.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return ""
    

class HookshotItem(InventoryItem):
  name = "hookshot"
  itemID = INVENTORY.INVENTORY_HOOKSHOT.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return ""
    

class OcarinaItem(InventoryItem):
  name = "ocarina"
  itemID = INVENTORY.INVENTORY_OCARINA.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return self.zelda.getCurSong()
    

class BoomerngItem(InventoryItem):
  name = "boomerang"
  itemID = INVENTORY.INVENTORY_BOOMERANG.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return ""
    

class MagicrodItem(InventoryItem):
  name = "magicRod"
  itemID = INVENTORY.INVENTORY_MAGIC_ROD.value

  def __init__(self, canvas, zelda: LinksAwakeningWrapper, x, y, width, height):
    super().__init__(canvas, zelda, x, y, width, height)
  
  def getNewText(self):
    return ""
  