from pyboy.plugins.base_plugin import PyBoyGameWrapper
from pyboy import PyBoy
from typing import cast
from pprint import pprint as print
from lib.util.structs import *
from lib.util.enums import *
from lib.util.scores import SCORES

class LinksAwakeningWrapper():
  cartridge_title = "ZELDA"
  def __init__(self, pyboy:PyBoy):
    from lib.gui.stateWindow import Window
    self.base = cast(PyBoyGameWrapper, pyboy.game_wrapper)
    self.pyboy = pyboy
    self.base._set_dimensions(0, 0, 21, 19, False)
    self.base.game_area_mapping(self.base.mapping_one_to_one, 0)
    self.ui:Window = None
    self.idlePenalty=0
    self.lastScore=0
  
  def link_ui(self, ui):
    self.ui = ui

  def name_input(self, name="Link", render=False):
    # Assume cursor is at 'A'
    # Name entry is like:
    # 
    # ABCDEFG  abcdefg
    # HIJKLMN  hijklmn
    # OPQRSTU  opqrstu
    # VWXYZ    vwxyz
    alpha = [
      "ABCDEFG  abcdefg",
      "HIJKLMN  hijklmn",
      "OPQRSTU  opqrstu",
      "VWXYZ    vwxyz"
    ]
    cur = (0,0)
    for c in name:
      for y,l in enumerate(alpha):
        x = l.find(c)
        if x != -1:
          break
      if x == -1:
        raise RuntimeError("Invalid name!")
      delta = (x-cur[0],y-cur[1])
      for i in range(abs(delta[0])):
        if delta[0] < 0:
          self.pyboy.button("left")
          self.advance(2, render)
        else:
          self.pyboy.button("right")
          self.advance(2, render)
      for i in range(abs(delta[1])):
        if delta[1] < 0:
          self.pyboy.button("up")
          self.advance(2, render)
        else:
          self.pyboy.button("down")
          self.advance(2, render)
      self.pyboy.button("a")
      self.advance(2, render)
      cur = (x,y)
    self.pyboy.button("start")
    self.advance(2, render)

  def start_game(self):
    print("starting")
    self.advance(180)
    self.pyboy.button("start")
    self.advance(60)
    self.pyboy.button("start")
    self.advance(30)
    self.pyboy.button("a")
    self.advance(15)
    self.name_input()
    self.advance(30)
    self.pyboy.button("a")
    self.advance(660)
    for i in range(20):
      self.advance(30)
      self.pyboy.button("a")
    self.pyboy.button("right")
    self.advance(10)
    self.printAllStats()
    self.holdButton("down", 30)
    self.printAllStats()
    self.holdButton("right", 70)
    self.printAllStats()
    for i in range(30):
      self.advance(30)
      self.pyboy.button("a")
    self.holdButton("left", 25)
    self.printAllStats()
    self.holdButton("down", 60)
    self.advance(60, True)
    self.printAllStats()
    for _ in range(9):
      self.holdButton("down", 10, True)
      self.printAllStats()



    self.base.start_game()

  def advance(self, frames=1, render=True):
    for _ in range(frames):
      self.pyboy.tick(1, render, render)

  def holdButton(self, btn, time, render=False):
    self.pyboy.button(btn, time)
    self.advance(time, render)
    
  def getOAMBuffer(self) -> tuple[list[OAMEntry],list[OAMEntry]]:
    # Returns Link, Other
    link = [
      OAMEntry(
        y=self.pyboy.memory[0xc000+4*i],
        x=self.pyboy.memory[0xc001+4*i],
        tile=self.pyboy.memory[0xc002+4*i],
        attr=self.pyboy.memory[0xc003+4*i])
      for i in range(12)
    ]
    other = [
      OAMEntry(
        y=   self.pyboy.memory[0xc030+4*i],
        x=   self.pyboy.memory[0xc031+4*i],
        tile=self.pyboy.memory[0xc032+4*i],
        attr=self.pyboy.memory[0xc033+4*i])
      for i in range(28)
    ]
    return link, other

  def decodeNumbers(self, n):
    # Numbers are stored as a weird hex encoded value
    # EG 0x11==0d17 will be stored as 0d23==0x17 
    return int(hex(n)[2:],10)

  def getEntities(self):
    return [
      Entity(
        x=self.pyboy.memory[0xc200+i] * (-1 if self.pyboy.memory[0x220+i] == 255 else 1),
        y=self.pyboy.memory[0xc210+i] * (-1 if self.pyboy.memory[0x230+i] == 255 else 1),
        z=self.pyboy.memory[0xc310+i],
        xVel=self.pyboy.memory[0xc240+i],
        yVel=self.pyboy.memory[0xc250+i],
        zVel=self.pyboy.memory[0xc320+i],
        xAcc=self.pyboy.memory[0xc260+i],
        yAcc=self.pyboy.memory[0xc270+i],
        zAcc=self.pyboy.memory[0xc330+i],
        status=self.pyboy.memory[0xc280+i],
        state=self.pyboy.memory[0xc290+i],
        colState=self.pyboy.memory[0xc2a0+i],
        intState1=self.pyboy.memory[0xc2b0+i],
        intState2=self.pyboy.memory[0xc2c0+i],
        intState3=self.pyboy.memory[0xc2d0+i],
        intState4=self.pyboy.memory[0xc390+i],
        intState5=self.pyboy.memory[0xc440+i],
        transition=self.pyboy.memory[0xc2e0+i],
        countdown1=self.pyboy.memory[0xc2f0+i],
        countdown2=self.pyboy.memory[0xc300+i],
        countdown3=self.pyboy.memory[0xc480+i],
        physicsFlags=self.pyboy.memory[0xc340+i],
        hitboxFlags=self.pyboy.memory[0xc350+i],
        health=self.pyboy.memory[0xc360+i],
        unk=self.pyboy.memory[0xc370+i],
        dir=self.pyboy.memory[0xc380+i],
        type=self.pyboy.memory[0xc3a0+i],
        variant=self.pyboy.memory[0xc3b0+i],
        recoilX=self.pyboy.memory[0xc3f0+i],
        recoilY=self.pyboy.memory[0xc400+i],
        iFrames=self.pyboy.memory[0xc410+i],
        drop=self.pyboy.memory[0xc4e0+i],
        hitbox=Hitbox(
          x=self.pyboy.memory[0xd580+i*4],
          y=self.pyboy.memory[0xd581+i*4],
          width=self.pyboy.memory[0xd582+i*4],
          height=self.pyboy.memory[0xd583+i*4],
        )
      )
      for i in range(16)
    ]

  def getCurHearts(self):
    return self.pyboy.memory[0xdb5a]
    
  def getMaxHearts(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb5b])
  
  def getRoomObjects(self):
    # Probably needs to be parsed into actual objects
    return [
      self.pyboy.memory[0xd700+i*16:0xd710+i*16] for i in range(16)
    ]
  
  def getCurrentEquip(self):
    #A,B
    return self.pyboy.memory[0xdb01],self.pyboy.memory[0xdb00]
  
  def getUnequip(self):
    return self.pyboy.memory[0xdb02:0xdb0b]
  
  def getInventoryRaw(self):
    return self.pyboy.memory[0xdb00:0xdb0b]

  def getInventory(self):
    rawItems = self.getInventoryRaw()
    flags = self.getFlags()
    return Inventory(
      sword=self.getSwordLevel()*int(INVENTORY.INVENTORY_SWORD.value in rawItems),
      shield=self.getShieldLevel()*int(INVENTORY.INVENTORY_SHIELD.value in rawItems),
      powder=self.getPowderCount()*int(INVENTORY.INVENTORY_MAGIC_POWDER.value in rawItems),
      bombs=self.getBombCount()*int(INVENTORY.INVENTORY_BOMBS.value in rawItems),
      brace=self.getBraceletLevel()*int(INVENTORY.INVENTORY_POWER_BRACELET.value in rawItems),
      bow=self.getArrowCount()*int(INVENTORY.INVENTORY_BOW.value in rawItems),

      roc=int(INVENTORY.INVENTORY_ROCS_FEATHER.value in rawItems),
      boots=int(INVENTORY.INVENTORY_PEGASUS_BOOTS.value in rawItems),
      shovel=int(INVENTORY.INVENTORY_SHOVEL.value in rawItems),
      hookshot=int(INVENTORY.INVENTORY_HOOKSHOT.value in rawItems),
      ocarina=int(INVENTORY.INVENTORY_OCARINA.value in rawItems),
      boomerang=int(INVENTORY.INVENTORY_BOOMERANG.value in rawItems),
      magicRod=int(INVENTORY.INVENTORY_MAGIC_ROD.value in rawItems),

      heartPieces=self.getHeartPieces(),
      tradeItem=self.getTradeItem(),
      seashells=self.getSeashells(),

      flippers=flags.hasFlippers,
      medicine=flags.hasMedicine,
      tailKey=flags.hasTailKey,
      slimeKeyOrLeaves=flags.hasSlimeKey,
      anglerKey=flags.hasFishKey,
      faceKey=flags.hasFaceKey,
      birdKey=flags.hasBirdKey
    )

  def getRecentRooms(self):
    return self.pyboy.memory[0xce81:0xce87]

  def getDungeonMinimap(self):
    return [
      self.pyboy.memory[0xd480+i*12:0xd488+i*12] for i in range(12)
    ]

  def getPositionHistory(self):
    return [
      PositionHistory(
        X=self.pyboy.memory[0xd155+i],
        Y=self.pyboy.memory[0xd175+i],
        Z=self.pyboy.memory[0xd195+i],
        D=self.pyboy.memory[0xd1b5+i],
      )
      for i in range(0x20)
    ]

  def getFlags(self):
    return GameFlags(
      lostInWoods=self.pyboy.memory[0xc10c],
      gelsStuck=self.pyboy.memory[0xc117],
      linkMovement=self.pyboy.memory[0xc11c],
      groundStatus=self.pyboy.memory[0xc11f],
      spinCharge=self.pyboy.memory[0xc122],
      collision=self.pyboy.memory[0xc133],
      swordState=self.pyboy.memory[0xc137],
      isPushing=self.pyboy.memory[0xc145],
      isAirborne=self.pyboy.memory[0xc146],
      isRunning=self.pyboy.memory[0xc14a],
      bootsCharge=self.pyboy.memory[0xc14b],
      placedBomb=self.pyboy.memory[0xc14e],
      isShielding=self.pyboy.memory[0xc15b],
      isCarrying=self.pyboy.memory[0xc15c],
      facingDir=self.pyboy.memory[0xc15d],
      canAction=self.pyboy.memory[0xc1ad],
      pitCounter=self.pyboy.memory[0xc1bb],
      itemCooldown=self.pyboy.memory[0xc1c0],
      switchPressed=self.pyboy.memory[0xc1cb],
      dialogWaiting=self.pyboy.memory[0xc1cc],
      shopItem1=self.pyboy.memory[0xc505],
      shopItem2=self.pyboy.memory[0xc506],
      shopItem3=self.pyboy.memory[0xc507],
      shopItem4=self.pyboy.memory[0xc508],
      shopItemPicked=self.pyboy.memory[0xc509],
      blockItems=self.pyboy.memory[0xc50a],
      shopIndexPicked=self.pyboy.memory[0xc50b],
      marinStatus=self.pyboy.memory[0xc50f],
      liftedEnemyType=self.pyboy.memory[0xc5a8],
      eggMazeProg=self.pyboy.memory[0xc5aa],
      hasFlippers=self.pyboy.memory[0xdb0c],
      hasMedicine=self.pyboy.memory[0xdb0d],
      hasTailKey=self.pyboy.memory[0xdb11],
      hasFishKey=self.pyboy.memory[0xdb12],
      hasFaceKey=self.pyboy.memory[0xdb13],
      hasBirdKey=self.pyboy.memory[0xdb14],
      hasSlimeKey=self.pyboy.memory[0xdb15],
      wanted=self.pyboy.memory[0xdb46],
      tarinStatus=self.pyboy.memory[0xdb48],
      songs=self.pyboy.memory[0xdb49],
      hasToadstool=self.pyboy.memory[0xdb4b],
      richardSpoken=self.pyboy.memory[0xdb55],
      bowWow=self.pyboy.memory[0xdb56],
      isThief=self.pyboy.memory[0xdb6e],
      marinFollows=self.pyboy.memory[0xdb73],
      marinInAnimalVil=self.pyboy.memory[0xdb74],
      ghostFollowing=self.pyboy.memory[0xdb79],
      ghostStep2=self.pyboy.memory[0xdb7a],
      roosterFollowing=self.pyboy.memory[0xdb7b],
      eggMaze=self.pyboy.memory[0xdb7c],
      inTrade=self.pyboy.memory[0xdb7f],
      isIndoors=self.pyboy.memory[0xdba5],
      finalForm=self.pyboy.memory[0xd219],
      signpostMazeGoal=self.pyboy.memory[0xd472],
      signpostMazeCur=self.pyboy.memory[0xd473],
      powerup=self.pyboy.memory[0xd47c],
      tileGlint=self.pyboy.memory[0xffb9],
      dialog=self.pyboy.memory[0xC19F],
      jingle=self.pyboy.memory[0xFFF2],
      waveSfx=self.pyboy.memory[0xFFF3],
      noiseSfx=self.pyboy.memory[0xFFF4],
    )
  
  def getInvCursorPos(self):
    return self.pyboy.memory[0xdba3]

  def getRoomWarps(self):
    return [
      RoomWarp(
        mapCat=self.pyboy.memory[0xd401+0+i*5],
        map=self.pyboy.memory[0xd401+1+i*5],
        room=self.pyboy.memory[0xd401+2+i*5],
        X=self.pyboy.memory[0xd401+3+i*5],
        Y=self.pyboy.memory[0xd401+4+i*5],
        tileIdx=self.pyboy.memory[0xd416+i]
      )
      for i in range(4)
    ]

  def getRoomObjects(self):
    return [
      self.pyboy.memory[0xd700+i*16:0xd710+i*16] for i in range(16)
    ]

  def getOverworldRoomStatus(self):
    return [
      self.pyboy.memory[0xd800+i*16:0xd810+i*16] for i in range(16)
    ]

  def getIndoorARoomStatus(self):
    return [
      self.pyboy.memory[0xd900+i*16:0xd910+i*16] for i in range(16)
    ]

  def getIndoorBRoomStatus(self):
    return [
      self.pyboy.memory[0xda00+i*16:0xda10+i*16] for i in range(16)
    ]

  def getKillCount(self):
    return self.pyboy.memory[0xd415]

  def getDungeonItems(self):
    return [
      DungeonItems(
        map=self.pyboy.memory[0xdb16+0+i*5],
        compass=self.pyboy.memory[0xdb16+1+i*5],
        beak=self.pyboy.memory[0xdb16+2+i*5],
        bossKey=self.pyboy.memory[0xdb16+3+i*5],
        smallKeys=self.pyboy.memory[0xdb16+4+i*5],
      )
      for i in range(8)
    ]
  
  def getShieldLevel(self):
    return self.decodeNumbers(self.pyboy.memory[0xc15a])

  def getTradeItem(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb0e])
  
  def getSeashells(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb0f])
  
  def getBraceletLevel(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb43])
  
  def getShieldLevel(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb44])
  
  def getArrowCount(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb45])
  
  def getCurSong(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb4a])
  
  def getPowderCount(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb4c])
  
  def getBombCount(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb4d])
  
  def getSwordLevel(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb4e])
  
  def getHeartPieces(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb5c])
  
  def getRupees(self):
    return RupeeCount(self.decodeNumbers(self.pyboy.memory[0xdb5e]),self.decodeNumbers(self.pyboy.memory[0xdb5d]))
  
  def getBossFlags(self):
    return self.pyboy.memory[0xdb65:0xdb6d]
  
  def getWreckingBallStatus(self):
    return WreckingBallStatus(
      room=self.pyboy.memory[0xdb6f],
      x=self.pyboy.memory[0xdb70],
      y=self.pyboy.memory[0xdb71],
      pillars=self.pyboy.memory[0xdb72],
    )

  def getMaxPowder(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb76])

  def getMaxBombs(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb77])

  def getMaxArrows(self):
    return self.decodeNumbers(self.pyboy.memory[0xdb78])
  
  def getCurrentBank(self):
    return self.pyboy.memory[0xdbaf]
  
  def getMapEnterPoint(self):
    return self.pyboy.memory[0xdbb1], self.pyboy.memory[0xdbb2]
  
  def getKillOrder(self):
    return self.pyboy.memory[0xdbb6:0xdbc6]
  
  def getCurrentDungeonItems(self):
    return DungeonItems(
        map=self.pyboy.memory[0xdbcc],
        compass=self.pyboy.memory[0xdbcd],
        beak=self.pyboy.memory[0xdbce],
        bossKey=self.pyboy.memory[0xdbcf],
        smallKeys=self.pyboy.memory[0xdbd0],
    )
  
  def getBossStatus(self):
    return [
      self.pyboy.memory[0xd900+0x06] & 0x20,
      self.pyboy.memory[0xd900+0x2b] & 0x20,
      self.pyboy.memory[0xd900+0x5a] & 0x20,
      self.pyboy.memory[0xd900+0xff] & 0x20,
      self.pyboy.memory[0xd900+0x85] & 0x20,
      self.pyboy.memory[0xd900+0xbc] & 0x20,
      self.pyboy.memory[0xda00+0xe8] & 0x20,
      self.pyboy.memory[0xda00+0x34] & 0x20,
    ]
  
  def getLinkStats(self):
    return LinkStatus(
      x=self.pyboy.memory[0xff98],
      y=self.pyboy.memory[0xff99],
      z=self.pyboy.memory[0xffa2],
      xVel=self.pyboy.memory[0xff9a],
      yVel=self.pyboy.memory[0xff9b],
      zVel=self.pyboy.memory[0xffa3],
      physics=self.pyboy.memory[0xff9c],
      state=self.pyboy.memory[0xff9d],
      dir=self.pyboy.memory[0xff9e],
      blocked=self.pyboy.memory[0xffa1],
      slowed=self.pyboy.memory[0xffb2],
      timer=self.pyboy.memory[0xffb7],
      mapRoom=self.pyboy.memory[0xfff6],
      mapID=self.pyboy.memory[0xfff7],
      roomStatus=self.pyboy.memory[0xfff8],
      sideScrolling=self.pyboy.memory[0xfff9],
      roomPos=self.pyboy.memory[0xfffa],
      finalRoomPos=self.pyboy.memory[0xfffb],
      overworldRoomID=self.pyboy.memory[0xdb54]
    )

  def getCurrentStairs(self):
    return Stairs(
      state=self.pyboy.memory[0xffac],
      x=self.pyboy.memory[0xffad],
      y=self.pyboy.memory[0xffae],
    )
  
  def printAllStats(self):
    from pprint import pprint
    # self.drawStats()
    # flags = {k:v for k,v in self.getFlags().items() if v}
    # pprint(f"Set Flags: ")
    # pprint(flags)
    # pprint(f"Cur Stairs: ")
    # pprint(self.getCurrentStairs())
    # pprint(f"Link State: ")
    # pprint(self.getLinkStats())
    # pprint(f"OAM Buffer: ")
    # pprint(self.getOAMBuffer())
    pprint(f"Entities: ")
    pprint([ e for e in self.getEntities() if e.status])
    # pprint(f"Cur Hearts: ")
    # pprint(self.getCurHearts())
    # pprint(f"Max Hearts: ")
    # pprint(self.getMaxHearts())
    # pprint(f"Room Objects: ")
    # pprint(self.getRoomObjects())
    # pprint(f"Room Warps: ")
    # pprint(self.getRoomWarps())
    # pprint(f"Current Equipment: ")
    # pprint(self.getCurrentEquip())
    # pprint(f"Inventory: ")
    # pprint(self.getInventory())
    # pprint(f"Recent Rooms: ")
    # pprint(self.getRecentRooms())
    # pprint(f"Minimap: ")
    # pprint(self.getDungeonMinimap())
    # pprint(f"Dungeon Items: ")
    # pprint(self.getDungeonItems())
    # pprint(f"Position History: ")
    # pprint(self.getPositionHistory())
    # pprint(f"Overworld: ")
    # pprint(self.getOverworldRoomStatus())
    # pprint(f"IndoorA: ")
    # pprint(self.getIndoorARoomStatus())
    # pprint(f"IndoorB: ")
    # pprint(self.getIndoorBRoomStatus())
    # pprint(f"Kill Count: ")
    # pprint(self.getKillCount())
    # pprint(f"Kill Order: ")
    # pprint(self.getKillOrder())
  
  def getFrameScore(self):
    # Penalize spending time without making progress
    return self.idlePenalty*SCORES["frame"]

  def getRupeeScore(self):
    # Reward collecting rupees. This may need more tweaking
    return self.getRupees().count*SCORES["rupee"]

  def getCurrentEntitiesScore(self):
    # Penalize number of entities on screen. The goal is to guide the player to killing enemies and collecting rewards
    activeEntities = [e for e in self.getEntities() if e.status != ENTITY_STATUS.ENTITY_STATUS_DISABLED.value]
    return len(activeEntities)*SCORES["entities"]

  def getDungeonScore(self):
    from lib.util.utils import getDungeonItems, getOpenDungeons

    # Reward dungeon progress
    score = 0
    openList = getOpenDungeons(self)
    itemList = getDungeonItems(self)
    for i,d in enumerate(self.getDungeonItems()):
      if openList[i]:
        score += SCORES["dungeonOpen"]
      if itemList[i]:
        score += SCORES["dungeonItem"]
      if d.beak:
        score += SCORES["dungeonBeak"]
      if d.compass:
        score += SCORES["dungeonCompass"]
      if d.map:
        score += SCORES["dungeonMap"]
      if d.bossKey:
        score += SCORES["dungeonBKey"]
      if self.getBossFlags()[i] & 1:
        score += SCORES["dungeonMidbossDefeat"]
      if self.getBossStatus()[i] & 1:
        score += SCORES["dungeonBossDefeat"]
      if self.getBossFlags()[i] & 2:
        score += SCORES["dungeonInstrument"]
    return score
  
  def getMapScore(self):
    # Reward exploration, more score per room visited
    score = 0
    score += sum(SCORES["overworldMap"] for r in self.getOverworldRoomStatus() for x in r if x)
    score += sum(SCORES["indoorMapA"] for r in self.getIndoorARoomStatus() for x in r if x)
    score += sum(SCORES["indoorMapB"] for r in self.getIndoorBRoomStatus() for x in r if x)
    return score
  
  def getFlagsScore(self):
    # Reward story progression
    flags = self.getFlags()
    score = 0
    score += flags.lostInWoods * -SCORES["lostInWoods"]
    score += flags.gelsStuck * -SCORES["gelsStuck"]
    score += flags.shopItem1 * SCORES["shopItem1"]
    score += flags.shopItem2 * SCORES["shopItem2"]
    score += flags.shopItem3 * SCORES["shopItem3"]
    score += flags.shopItem4 * SCORES["shopItem4"]
    score += flags.marinStatus * SCORES["marinStatus"]
    score += flags.eggMazeProg * SCORES["eggMazeProg"]
    score += flags.hasFlippers * SCORES["hasFlippers"]
    score += flags.hasMedicine * SCORES["hasMedicine"]
    score += flags.hasTailKey * SCORES["hasTailKey"]
    score += flags.hasFishKey * SCORES["hasFishKey"]
    score += flags.hasFaceKey * SCORES["hasFaceKey"]
    score += flags.hasBirdKey * SCORES["hasBirdKey"]
    score += flags.hasSlimeKey * SCORES["hasSlimeKey"]
    score += flags.tarinStatus * SCORES["tarinStatus"]
    score += flags.songs * SCORES["songs"]
    score += flags.hasToadstool * SCORES["hasToadstool"]
    score += flags.richardSpoken * SCORES["richardSpoken"]
    score += flags.bowWow * SCORES["bowWow"]
    score += flags.marinFollows * SCORES["marinFollows"]
    score += flags.marinInAnimalVil * SCORES["marinInAnimalVil"]
    score += flags.ghostFollowing * SCORES["ghostFollowing"]
    score += flags.ghostStep2 * SCORES["ghostStep2"]
    score += flags.roosterFollowing * SCORES["roosterFollowing"]
    score += flags.eggMaze * SCORES["eggMaze"]
    score += flags.finalForm * SCORES["finalForm"]
    score += flags.signpostMazeGoal * SCORES["signpostMazeGoal"]
    score += flags.signpostMazeCur * SCORES["signpostMazeCur"]
    score += flags.powerup * SCORES["powerup"]
    score += flags.tileGlint * SCORES["tileGlint"]
    return score

  def getInventoryScore(self):
    # Reward having items, this includes having consumables and passive items
    score = 0
    inv = self.getInventory()
    score += inv.sword * SCORES["sword"]
    score += inv.shield * SCORES["shield"]
    score += inv.brace * SCORES["brace"]
    score += inv.ocarina * SCORES["ocarina"]
    score += inv.powder * SCORES["powder"]
    score += inv.bow * SCORES["bow"]
    score += inv.bombs * SCORES["bombs"]
    score += inv.roc * SCORES["roc"]
    score += inv.boots * SCORES["boots"]
    score += inv.shovel * SCORES["shovel"]
    score += inv.magicRod * SCORES["magicRod"]
    score += inv.hookshot * SCORES["hookshot"]
    score += inv.tradeItem * SCORES["tradeItem"]
    score += inv.boomerang * SCORES["boomerang"]
    score += inv.flippers * SCORES["flippers"]
    score += inv.tailKey * SCORES["tailKey"]
    score += inv.slimeKeyOrLeaves * SCORES["slimeKeyOrLeaves"]
    score += inv.anglerKey * SCORES["anglerKey"]
    score += inv.faceKey * SCORES["faceKey"]
    score += inv.birdKey * SCORES["birdKey"]
    score += inv.medicine * SCORES["medicine"]
    score += inv.seashells * SCORES["seashells"]
    score += inv.heartPieces * SCORES["heartPieces"]

    return score

  def getHealthScore(self):
    return self.getCurHearts() * SCORES["health"]

  def getScore(self):
    '''
    We want to reward progression without promoting loops or local maxima.
    No fixed range, everything will be relative. 
    '''
    score = self.getRupeeScore() + self.getCurrentEntitiesScore() + \
    self.getDungeonScore() + self.getMapScore() + self.getFlagsScore() + self.getHealthScore()
    
    if score > self.lastScore:
      self.idlePenalty = 0
      self.lastScore = score
    else:
      self.idlePenalty += 1

    return score + self.getFrameScore()