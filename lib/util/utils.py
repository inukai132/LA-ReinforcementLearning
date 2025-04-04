from lib.wrapper.LinksAwakeningWrapper import LinksAwakeningWrapper

def getOpenDungeons(zelda: LinksAwakeningWrapper):
  return [
    zelda.getInventory().tailKey,
    zelda.getFlags().bowWow & 1 or zelda.getInventory().boomerang or zelda.getInventory().hookshot or zelda.getInventory().magicRod,
    zelda.getInventory().slimeKeyOrLeaves >= 6,
    zelda.getInventory().anglerKey,
    zelda.getInventory().flippers,
    zelda.getInventory().faceKey,
    zelda.getInventory().birdKey,
    zelda.getInventory().shield >= 2 
  ]

def getDungeonItems(zelda: LinksAwakeningWrapper):
  return [
    zelda.getInventory().roc,
    zelda.getInventory().brace,
    zelda.getInventory().boots,
    zelda.getInventory().flippers,
    zelda.getInventory().hookshot,
    zelda.getInventory().brace >= 2,
    zelda.getInventory().shield >= 2,
    zelda.getInventory().magicRod
  ]

