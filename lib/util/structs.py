from dataclasses import dataclass

@dataclass
class OAMEntry:
  x: int
  y: int
  tile: int
  attr: int

@dataclass
class Hitbox:
  x: int
  y: int
  width: int
  height: int

@dataclass
class Entity:
  x:int
  y:int
  z:int
  xVel:int
  yVel:int
  zVel:int
  xAcc:int
  yAcc:int
  zAcc:int
  status:int
  state:int
  colState:int
  transition:int
  intState1:int
  intState2:int
  intState3:int
  intState4:int
  intState5:int
  countdown1:int
  countdown2:int
  countdown3:int
  physicsFlags:int
  hitboxFlags:int
  health:int
  unk:int
  dir:int
  type:int
  variant:int
  recoilX:int
  recoilY:int
  iFrames:int
  drop:int
  hitbox:Hitbox

@dataclass
class PositionHistory:
  X:int
  Y:int
  Z:int
  D:int

@dataclass
class GameFlags:
  lostInWoods:int
  gelsStuck:int
  linkMovement:int
  groundStatus:int
  spinCharge:int
  collision:int
  swordState:int
  isPushing:int
  isAirborne:int
  isRunning:int
  bootsCharge:int
  placedBomb:int
  isShielding:int
  isCarrying:int
  facingDir:int
  canAction:int
  pitCounter:int
  itemCooldown:int
  switchPressed:int
  dialogWaiting:int
  shopItem1:int
  shopItem2:int
  shopItem3:int
  shopItem4:int
  shopItemPicked:int
  blockItems:int
  shopIndexPicked:int
  marinStatus:int
  liftedEnemyType:int
  eggMazeProg:int
  hasFlippers:int
  hasMedicine:int
  hasTailKey:int
  hasFishKey:int
  hasFaceKey:int
  hasBirdKey:int
  hasSlimeKey:int
  wanted:int
  tarinStatus:int
  songs:int
  hasToadstool:int
  richardSpoken:int
  bowWow:int
  isThief:int
  marinFollows:int
  marinInAnimalVil:int
  ghostFollowing:int
  ghostStep2:int
  roosterFollowing:int
  eggMaze:int
  inTrade:int
  isIndoors:int
  finalForm:int
  signpostMazeGoal:int
  signpostMazeCur:int
  powerup:int
  tileGlint:int

@dataclass
class RoomWarp:
  mapCat:int
  map:int
  room:int
  X:int
  Y:int
  titleIdx:int

@dataclass
class DungeonItems:
  map:bool
  compass:bool
  beak:bool
  bossKey:bool
  smallKeys:int

class RupeeCount:
  def __init__(self, lo, hi):
    self.hi = hi
    self.lo = lo
    self.count = hi*256+lo
  
@dataclass
class WreckingBallStatus:
  x: int
  y: int
  room: int
  pillars: int

@dataclass
class LinkStatus:
  x:int
  y:int
  z:int
  xVel:int
  yVel:int
  zVel:int
  physics:int
  state:int
  dir:int
  blocked:int
  slowed:int
  timer:int
  mapRoom:int
  mapID:int
  roomStatus:int
  sideScrolling:int
  roomPos:int
  finalRoomPos:int

@dataclass
class Stairs:
  x: int
  y: int
  state: int